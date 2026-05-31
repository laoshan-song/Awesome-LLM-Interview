# LoRA 及参数高效微调（PEFT）

## 面试高频考点
- LoRA 的原理是什么？为什么有效？
- rank (r) 和 lora_alpha 怎么选？
- LoRA 和全量微调的区别？
- QLoRA 的三大技术改进？
- LoRA 加在哪些层？为什么？

---

## 一、为什么需要 PEFT？

全量微调（Full Fine-tuning）的问题：

| 模型规模 | 全量微调显存 | 问题 |
|---------|------------|------|
| LLaMA-2 7B | ~56 GB (Adam) | 需要 A100 (80GB) |
| LLaMA-2 70B | ~560 GB | 需要 8×A100 |
| DeepSeek-V3 671B | ~5 TB+ | 基本不可行 |

PEFT（Parameter-Efficient Fine-Tuning）：只训练少量参数，冻结大部分权重，将微调成本降低 100-1000 倍。

---

## 二、LoRA 核心原理

![LoRA 原理论文图：冻结主干并学习低秩更新](https://ar5iv.labs.arxiv.org/html/2106.09685/assets/x1.png)

> 图源：`LoRA: Low-Rank Adaptation of Large Language Models` 论文 HTML 图。

### 数学基础：低秩假设

LoRA 的核心假设：预训练权重的**更新矩阵 ΔW 具有低秩特性**。

```
全量微调：W' = W + ΔW（ΔW 是 d×k 的完整矩阵，参数量 d×k）

LoRA 微调：W' = W + B·A
  其中 B ∈ R^{d×r}, A ∈ R^{r×k}, r << min(d, k)
  
  参数量：d×r + r×k = r×(d+k)  vs  全量：d×k
  节省率 ≈ d×k / r(d+k) ≈ min(d,k) / (2r)
```

### 为什么这个假设成立？

Aghajanyan et al. (2021) 的"内在维度"研究表明：预训练语言模型在适应下游任务时，权重更新实际上可以在**极低维度的子空间**中完成。一个 175B 模型的微调，在仅几百维的子空间中进行就能达到接近全量微调的效果。

这不意味着"ΔW 恰好是低秩的"，而是说"低秩近似已经足够好"。

### 具体实现

```
原始前向（冻结部分）：
  h = W₀ · x                    （W₀ 冻结，不更新）

LoRA 旁路（可训练部分）：
  Δh = B · A · x                （只训练 A 和 B）

输出：
  h' = h + Δh = W₀ · x + B · A · x

初始化：
  A ~ N(0, σ²)   （随机高斯初始化，小方差）
  B = 0           （零初始化 → 初始时 Δh = 0，不影响预训练模型输出）

缩放：
  Δh = (α/r) · B · A · x        （α 是缩放因子，控制 LoRA 的贡献强度）
```

### 参数量对比

```
以 Attention 的 Q 投影矩阵为例，d_model=4096, r=16：

全量微调 Q 投影：
  W_Q ∈ R^{4096 × 4096} = 16,777,216 参数

LoRA Q 投影：
  B ∈ R^{4096 × 16} = 65,536 参数
  A ∈ R^{16 × 4096} = 65,536 参数
  合计 = 131,072 参数

节省 = 16,777,216 / 131,072 ≈ 128 倍（99.2% 参数节省）
```

### 面试里怎么把“低秩”讲得更像理解而不是背诵

一个比较好的说法是：

- 预训练模型已经学会了大部分通用表示
- 下游任务通常不是“重学整套知识”，而是对已有能力做小幅纠偏
- 所以很多有效更新可以压缩到一个更小的子空间里

这就是 LoRA 为什么常常能用极少参数逼近全量微调效果。

---

## 三、Rank 和 Alpha 的选择

### Rank (r) 怎么选？

| rank | 参数量 | 适用场景 | 效果 |
|------|--------|---------|------|
| r=4 | 极少 | 简单分类任务、情感分析 | 基本可用 |
| **r=8** | 少 | 通用指令微调 | 性价比高 |
| **r=16** | 中 | **常用默认值**，大多数任务 | 效果接近全量 |
| r=32 | 较多 | 复杂推理、代码、多任务 | 非常接近全量 |
| r=64 | 多 | 接近全量微调上限 | 几乎 = 全量 |
| r=128 | 很多 | 极限场景 | 等价全量但更省 |

**实际经验**：
- 原始 LoRA 论文：r=1~4 在很多任务上已经有效
- 工程实践：r=8~16 是最常用的平衡点
- 监控方式：从 r=8 开始，逐步增大，看验证集效果是否持续提升，不提升就停

### lora_alpha (α) 的作用

```
实际 LoRA 更新：Δh = (α/r) · B · A · x

α 控制 LoRA 输出的放大倍数

经验规则：α = 2r（如 r=8 → α=16, r=16 → α=32）
这样的好处：切换 rank 时不需要重新调整学习率

α 越大 → LoRA 的影响越大 → 更接近全量微调（但要防过拟合）
α 越小 → LoRA 的影响越小 → 更保守（保留更多预训练知识）
```

---

## 四、LoRA 加在哪些层？

### 原论文建议

原始 LoRA 论文只加在 **Attention 的 Q 和 V 投影矩阵**上：

```
对于每个 Attention 层：
  W_Q → W_Q + B_Q · A_Q    （LoRA on Q）
  W_V → W_V + B_V · A_V    （LoRA on V）
  W_K → 不修改（实验表明对结果影响不大）
  W_O → 不修改

FFN 层：不修改
```

### 后续扩展

| 方案 | 配置 | 适用场景 |
|------|------|---------|
| **Q + V only** | 原论文默认 | 大多数任务，参数最省 |
| **Q + K + V + O** | All attention | 需要更强表达力 |
| **Attention + FFN** | 所有线性层 | 最接近全量微调效果 |
| **LoRA on Embedding** | 额外加 Embedding 层 | 领域术语微调 |

**工程建议**：从 Q+V only 开始，效果不够再加。FFN 的 LoRA 对提升复杂推理有帮助但增加参数不少。

---

## 五、QLoRA

QLoRA = **4-bit 量化基础模型 + LoRA 微调**，三项关键技术：

### ① NF4（NormalFloat4）量化

不是简单的线性 INT4，而是针对**正态分布权重**优化的 4-bit 数据格式：

```
NF4 将有界正态分布的 CDF 均匀切分为 16 个区间
每个区间的期望值作为一个量化级别
这 16 个值就是 NF4 的量化值

对于正态分布数据（神经网络权重就是近似正态的）：
  NF4 的信息损失 < INT4

每个量化值独立存储，每个 block (64 权重) 共享一个 scale
```

### ② 双重量化（Double Quantization）

```
第一次量化：权重 → NF4 值（每 64 个权重共享一个 FP32 scale）
第二次量化：FP32 scale → FP8 值（再压缩量化常数本身）

每个参数额外节省：约 0.37 bit
对于一个 65B 模型 → 额外节省约 3 GB 显存
```

### ③ 分页优化器（Paged Optimizer）

```
利用 NVIDIA 统一内存（Unified Memory）：
  当 GPU 显存不足时 → 自动将优化器状态换出到 CPU RAM
  需要时 → 自动换回 GPU 显存

类似操作系统的虚拟内存分页机制
防止 OOM 但可能导致速度下降（CPU↔GPU 换页有延迟）
```

### QLoRA 效果

| 模型 | 方法 | 所需显存 | 精度 |
|------|------|---------|------|
| LLaMA 65B | 全量微调 | ~780 GB | 基线 |
| LLaMA 65B | LoRA (FP16) | ~195 GB | 接近基线 |
| LLaMA 65B | **QLoRA (NF4)** | **~48 GB** | 接近 LoRA (FP16) |

---

## 六、其他 PEFT 方法对比

| 方法 | 核心思路 | 可训练参数 | 推理开销 | 典型场景 |
|------|---------|-----------|---------|---------|
| **LoRA** | 低秩分解 ΔW = BA | ~0.1-1% | **零**（可合并） | 通用首选 |
| **QLoRA** | LoRA + NF4 量化 | ~0.1-1% | **零**（可合并） | 消费级 GPU 微调 |
| Adapter | 层间插入小型 MLP（串行） | ~1-5% | 有（串行瓶颈） | 早期方案 |
| Prefix Tuning | 在 K,V 前拼接可训练向量 | ~0.01% | 占用上下文 | 极低参数场景 |
| Prompt Tuning | 输入层拼接软 prompt | ~0.001% | 占用上下文 | 超低参数场景 |
| IA³ | 学习缩放向量（逐元素乘法） | ~0.01% | **零**（可合并） | 最轻量方案 |

### LoRA 的优势

1. **零推理开销**：`W' = W + BA` 可提前算好，推理时和原始模型完全一样
2. **多 Adapter 切换**：不同任务的 LoRA 权重（A,B）可以不合并，动态切换
3. **存储友好**：一个 LoRA adapter 只有几 MB（全量微调 checkpoint = 完整模型大小）
4. **可组合**：多个 LoRA 可以线性组合（LoRA 算术——如语言 LoRA + 任务 LoRA）

---

## 七、LoRA 进阶技巧

### LoRA+（更高效的训练）

```
发现：A 和 B 的学习率不应相同
A（输入侧矩阵）需要更大的学习率
B（输出侧矩阵）需要更小的学习率

λ = lr_B / lr_A ≈ 2^-4 ~ 2^-2

这样设置使收敛更快
```

### AdaLoRA（自适应 Rank）

```
问题：标准 LoRA 对所有层使用相同 rank，但不同层重要性不同

AdaLoRA 方案：
  - 用 SVD 分解 ΔW = P · Σ · Q
  - 训练时动态调整 Σ 对角线上的有效秩
  - 重要层自动获得更大的有效 rank
  - 不重要层的 rank 被压缩

效果：相同参数预算下，AdaLoRA > 统一 rank 的 LoRA
```

### DoRA（Weight-Decomposed LoRA）

```
将预训练权重分解为"方向"和"幅度"两部分：
  W = m · (W / ||W||) = 幅度 × 方向

  LoRA 只更新方向部分，幅度部分单独学习一个缩放向量

效果：DoRA 的学习模式更接近全量微调，性能优于标准 LoRA
```

---

## 工程补充

### LoRA 常见 target modules

实践里最常见的是：

- `q_proj`, `v_proj`：最经典默认配置
- `q_proj`, `k_proj`, `v_proj`, `o_proj`：想提高表达力时扩展
- `gate_proj`, `up_proj`, `down_proj`：复杂任务里也会加

面试里如果被问“LoRA 加哪几层”，最好顺手补一句：通常先从 attention 投影层开始，效果不够再扩到 FFN。

---

## 八、面试延伸

**Q：LoRA 为什么初始化 B=0？**

> 保证训练开始时 ΔW = A × B = A × 0 = 0。即 LoRA 层的初始输出与冻结的预训练模型完全一样，不引入任何随机噪声破坏预训练知识。随着训练进行，B 逐渐学到非零值，ΔW 开始起作用。这确保了训练起点的稳定性。

**Q：LoRA 在推理时有额外开销吗？**

> 没有！关键优势：可以将 LoRA 权重合并回原始模型 `W' = W + (α/r)·BA`，推理时和标准模型完全一样，零额外延迟。也可以保持分离，通过动态加载/卸载不同 LoRA 权重，支持单个模型实例同时服务多个 LoRA adapter（vLLM 的 Multi-LoRA Serving），每个请求可以用不同的 adapter。

**Q：全量微调和 LoRA 微调分别在什么场景下选择？**

> 选全量微调：数据量充足（10M+ tokens）、任务与预训练差异大（安全领域、多语言大幅扩展）、计算资源允许（追求最高效果上限）。选 LoRA：数据量较少（<1M tokens）、多任务需灵活切换 adapter、消费级硬件、防止过拟合和灾难性遗忘。指令微调用 LoRA 通常足够；需要深度领域知识融合时全量更可靠。实践中很多团队用 LoRA 做快速实验迭代，确定方向后才考虑全量微调。

**Q：什么场景下 LoRA 效果不好？**

> ① 任务与预训练知识差异极大（全新的语言、完全不同的领域），LoRA 的低秩约束可能限制了表达力；② 训练数据量巨大（100M+ tokens），此时全量微调的边际收益更高；③ 需要同时大幅改变模型的多项能力（如语言+推理+安全），单一 LoRA 可能不够。

---

## 原始论文

| 论文 | 链接 |
|------|------|
| LoRA: Low-Rank Adaptation of Large Language Models (Hu et al., ICLR 2022) | [arxiv.org/abs/2106.09685](https://arxiv.org/abs/2106.09685) |
| QLoRA: Efficient Finetuning of Quantized LLMs (Dettmers et al., NeurIPS 2023) | [arxiv.org/abs/2305.14314](https://arxiv.org/abs/2305.14314) |
| Intrinsic Dimensionality Explains the Effectiveness of LM Fine-Tuning (Aghajanyan et al., ACL 2021) | [arxiv.org/abs/2012.13255](https://arxiv.org/abs/2012.13255) |
| AdaLoRA: Adaptive Budget Allocation for Parameter-Efficient FT (Zhang et al., ICLR 2023) | [arxiv.org/abs/2303.10512](https://arxiv.org/abs/2303.10512) |
| DoRA: Weight-Decomposed Low-Rank Adaptation (Liu et al., ICML 2024) | [arxiv.org/abs/2402.09353](https://arxiv.org/abs/2402.09353) |

## 延伸阅读与视频

| 平台 | 标题 | 说明 |
|------|------|------|
| 📺 YouTube | [LoRA: Low-Rank Adaptation Paper Explained](https://www.youtube.com/watch?v=PXWYUTMt-AU) | Yannic Kilcher 论文精读含数学推导 |
| 📺 B站 | [Bilibili 搜索"LoRA 微调 原理"](https://search.bilibili.com/all?keyword=LoRA%E5%BE%AE%E8%B0%83%E5%8E%9F%E7%90%86&order=click) | 按播放量筛选中文讲解 |
