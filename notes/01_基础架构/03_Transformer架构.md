# Transformer 架构详解

## 面试高频考点
- Transformer 整体结构是什么？
- Self-Attention 的计算过程？复杂度？
- 为什么要除以 √d_k？
- Encoder-Decoder 和 Decoder-only 的区别？
- 残差连接和 Layer Norm 的作用？
- SwiGLU 为什么比 ReLU 好？

---

## 一、整体架构

### 原始 Transformer（Encoder-Decoder）

```
                    Encoder (×N)                      Decoder (×N)
              ┌──────────────────┐            ┌──────────────────────┐
  Input       │  Add & Norm       │            │  Add & Norm           │  Output
  ────────────│    ↑              │            │    ↑                  │────────→
              │  Feed Forward     │            │  Feed Forward         │
              │    ↑              │            │    ↑                  │
              │  Add & Norm       │            │  Add & Norm           │
              │    ↑              │            │    ↑                  │
              │  Multi-Head       │            │  Cross-Attention      │
              │  Self-Attention   │   ────────→│  (Q from Dec, KV from │
              │    ↑              │   KV from  │   Encoder output)     │
              │  Input Embedding  │   Encoder  │    ↑                  │
              └──────────────────┘            │  Add & Norm           │
                                              │    ↑                  │
                                              │  Masked Multi-Head    │
                                              │  Self-Attention       │
                                              │    ↑                  │
                                              │  Output Embedding     │
                                              └──────────────────────┘
```

### 现代 Decoder-only 架构（LLaMA 等）

```
Input → Embedding + Position Encoding
  ↓
[× L 层，每层结构如下：]
  ┌─────────────────────────┐
  │ 输入 x                   │
  │   ↓                     │
  │  RMSNorm(x)             │  ← Pre-Norm
  │   ↓                     │
  │  Multi-Head Attention   │  ← 带 Causal Mask
  │  (含 RoPE 位置编码)      │
  │   ↓                     │
  │  x + Attention(RMSNorm(x))│ ← 残差连接
  │   ↓                     │
  │  RMSNorm(x')            │  ← Pre-Norm
  │   ↓                     │
  │  FFN (SwiGLU)           │
  │   ↓                     │
  │  x' + FFN(RMSNorm(x'))  │  ← 残差连接
  │   ↓                     │
  │  输出（下一层输入）       │
  └─────────────────────────┘
  ↓
RMSNorm → Linear(d_model, vocab_size) → Softmax
```

---

## 二、Self-Attention 详解

### 计算步骤（逐张量维度）

```
输入：X ∈ R^{n × d_model}  （n 个 token，每个 d_model 维）

Step 1: 线性投影
  Q = X · W_Q    (W_Q ∈ R^{d_model × d_k})
  K = X · W_K    (W_K ∈ R^{d_model × d_k})
  V = X · W_V    (W_V ∈ R^{d_model × d_v})
  通常 d_k = d_v = d_model / h

Step 2: 计算注意力分数
  Scores = Q · K^T / √d_k    (∈ R^{n × n})
  除以 √d_k 防止 softmax 进入饱和区

Step 3: Causal Mask（Decoder-only）
  Mask[i, j] = -∞ if j > i else 0
  Masked_Scores = Scores + Mask

Step 4: Softmax 归一化
  Attention_Weights = softmax(Masked_Scores)    (∈ R^{n × n})
  每行是一个概率分布（对每个 query token 的注意力分布）

Step 5: 加权聚合 Value
  Output = Attention_Weights · V    (∈ R^{n × d_v})
```

### 为什么要除以 √d_k？

```
假设 Q 和 K 的每个分量独立同分布，均值为 0，方差为 1：

点积 q·k = Σ_{i=1}^{d_k} q_i · k_i

方差：Var(q·k) = Σ Var(q_i · k_i) = Σ Var(q_i) · Var(k_i) = d_k · 1

所以 q·k 的方差是 d_k！

当 d_k 较大时（如 128），q·k 的典型值在 ±√128 ≈ ±11 左右
Softmax 在 ±11 处已经极端饱和 → 梯度 ≈ 0

√d_k 缩放后：q·k/√d_k 的方差 ≈ 1，softmax 输入在合理范围
```

---

## 三、Multi-Head Attention 详细设计

### 参数量分析

以 LLaMA-2 7B 为例：d_model=4096, h=32, d_head=128

```
每个头的权重矩阵：
  W_Q_i, W_K_i, W_V_i 各 ∈ R^{4096 × 128}
  每头参数量 = 3 × 4096 × 128 ≈ 1.57M
  32 头合计 = 32 × 1.57M ≈ 50.3M

输出投影 W_O ∈ R^{4096 × 4096} ≈ 16.8M

MHA 总参数 = 50.3M + 16.8M ≈ 67.1M

（对比：单头 Attention 的参数量 = 4 × 4096 × 4096 ≈ 67.1M，完全一样！）
```

**关键洞察**：Multi-Head Attention 不增加参数量，只是把同一个大矩阵乘法拆成了多个小矩阵乘法并行执行，提供了更多样的表示空间。

### 不同头学到了什么？

实验观察（通过可视化注意力模式）：
- **头 0-3**：关注相邻 token（局部语法结构）
- **头 4-7**：关注句法依赖（主谓一致、介词短语附着）
- **头 20-23**：关注远距离语义关系（指代消解）
- **头 28-31**：关注特殊 token（分隔符、BOS、标点）

这是**自发涌现**的，非人为设计。

---

## 四、Causal Mask（因果掩码）

### 为什么需要？

Decoder-only 在训练时输入完整序列，但推理时只能逐 token 生成。Causal Mask 保证训练和推理行为一致——每个 token 只能利用它之前的信息。

```
Causal Mask 矩阵（n=5）：

      K₀  K₁  K₂  K₃  K₄
  Q₀ [ 0  -∞  -∞  -∞  -∞ ]  只能看到自己
  Q₁ [ 0   0  -∞  -∞  -∞ ]  只能看到前 2 个
  Q₂ [ 0   0   0  -∞  -∞ ]  只能看到前 3 个
  Q₃ [ 0   0   0   0  -∞ ]  只能看到前 4 个
  Q₄ [ 0   0   0   0   0 ]  能看到全部

0 = 保留，-∞ = 屏蔽（softmax(-∞) = 0）
```

---

## 五、FFN 与激活函数

### 从 ReLU 到 SwiGLU

```
原始 FFN（ReLU）：
  FFN(x) = ReLU(xW₁ + b₁)W₂ + b₂
  参数量：2 × d_model × d_ff

SwiGLU（LLaMA/Qwen/DeepSeek 使用）：
  FFN(x) = (Swish(xW_gate) ⊙ xW_up) · W_down
  其中 Swish(x) = x · σ(x)  （σ 为 sigmoid）
  参数量：3 × d_model × d_ff  （多了一个 gate 矩阵）

为保持参数量不变，LLaMA 将 d_ff 设为 8/3 × d_model ≈ 2.67d（而非原来的 4d）
```

### 为什么 SwiGLU 更好？

| 维度 | ReLU | SwiGLU |
|------|------|--------|
| 非线性 | 硬截断（负值→0） | 平滑门控 |
| 梯度 | 负值区梯度=0（死亡 ReLU） | 处处可微，梯度平滑 |
| 表达能力 | 简单阈值 | 门控机制，非线性更强 |
| 训练速度 | 快 | 略慢（多一个矩阵乘法） |
| 性能 | 基线 | 普遍优于 ReLU（+1-3% 下游） |

**直觉**：SwiGLU 的门控机制让 FFN 学会"选择性通过"信息（gate 接近 1 时通过，接近 0 时阻断），而非简单截断。

---

## 六、残差连接 & 归一化

### 残差连接的必要性

```
没有残差：h(x) = Sublayer(x)
有残差：h(x) = x + Sublayer(x)

反向传播时：
∂h/∂x = 1 + ∂Sublayer/∂x

那个 "+1" 保证了梯度至少为 1，不会因 Sublayer 梯度接近 0 而消失
这是 Transformer 能堆叠 80+ 层的基础
```

### Pre-Norm vs Post-Norm

```
Post-Norm（原始论文）：
  y = LayerNorm(x + Sublayer(x))
  问题：残差分支的输出方差未经控制，随深度累积放大 → 训练初期不稳定，需要学习率 warmup

Pre-Norm（现代 LLM）：
  y = x + Sublayer(LayerNorm(x))
  优势：先归一化再计算，主路径 x 的梯度始终有 +1 通道，训练稳定，无需 warmup

LLaMA 用 Pre-Norm + RMSNorm（去掉 LayerNorm 的均值中心化）
```

### RMSNorm vs LayerNorm

```
LayerNorm：
  y = (x - μ) / σ × γ + β
  需要计算均值 μ 和标准差 σ

RMSNorm：
  y = x / RMS(x) × γ
  RMS(x) = sqrt(mean(x²))
  只计算均方根，省去均值计算，速度提升 ~7%，性能相当
```

---

## 七、三种架构对比

| 维度 | Encoder-only | Decoder-only | Encoder-Decoder |
|------|-------------|-------------|-----------------|
| 代表 | BERT, RoBERTa | GPT, LLaMA, Qwen | T5, BART |
| 注意力 | 双向（看全句） | 单向因果 | Enc 双向 + Dec 交叉 |
| 预训练目标 | MLM（掩码预测） | Next Token Prediction | Span Corruption |
| 生成能力 | 差 | **最优** | 好 |
| 理解能力 | **最优** | 好（通过生成间接体现） | 好 |
| 当前地位 | 不再主流 | **绝对主流** | 少量使用 |

### 为什么 Decoder-only 统治了？

1. **统一任务格式**：文本生成、推理、对话都可统一为"给定前缀预测下一个 token"
2. **Scaling 友好**：Next Token Prediction 的监督信号密度高于 MLM
3. **In-Context Learning**：Decoder-only 天然支持 few-shot（拼接示例在前缀中）
4. **工程简单**：不需要 Encoder-Decoder 之间的交叉注意力，KV Cache 更直接

---

## 八、面试延伸

**Q：为什么现代 LLM 都用 Decoder-only？**

> ① 统一的任务表示——所有 NLP 任务都可建模为"给定前缀，预测后续"；② 因果注意力天然支持自回归生成，推理时无需额外适配；③ 工程简化，KV Cache 管理直接；④ 在 Scaling Law 下，Decoder-only 在相同计算预算下的下游性能通常优于 Encoder-Decoder。

**Q：Attention 的 KV Cache 是怎么工作的？**

> 自回归生成时，每步只需计算新 token 的 Q、K、V。历史 token 的 K 和 V 在之前步骤已计算过且不会改变（因果掩码保证了这一点），因此可以缓存复用。详见 [09_KV_Cache.md](../03_推理与优化/09_KV_Cache.md)。

**Q：Transformer 的位置编码为什么是必需的？**

> Self-Attention 本质是对输入进行加权求和，如果没有任何位置信息，打乱输入 token 顺序，Attention 输出完全一样（排列不变性）。位置编码将顺序信息注入模型，详见 [04_位置编码.md](./04_位置编码.md)。

**Q：为什么 Attention 需要 Q、K、V 三个投影，两个不行吗？**

> Q 和 K 负责计算"谁和谁相关"（匹配/检索），V 负责"相关的内容是什么"（取值）。分离 Q、K、V 让模型在两个子任务上使用不同的表示：查询-键匹配可能更关注短文本特征，而值的聚合可能更关注内容特征。这是 Multi-Head Attention 表达能力的关键来源。

---

## 原始论文

| 论文 | 链接 |
|------|------|
| Attention Is All You Need (Vaswani et al., NeurIPS 2017) | [arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762) |
| Root Mean Square Layer Normalization (Zhang & Sennrich, NeurIPS 2019) | [arxiv.org/abs/1910.07467](https://arxiv.org/abs/1910.07467) |
| SwiGLU: GLU Variants Improve Transformer (Shazeer, 2020) | [arxiv.org/abs/2002.05202](https://arxiv.org/abs/2002.05202) |
| FlashAttention (Dao et al., NeurIPS 2022) | [arxiv.org/abs/2205.14135](https://arxiv.org/abs/2205.14135) |

## 延伸阅读与视频

| 平台 | 标题 | 说明 |
|------|------|------|
| 📺 YouTube | [But what is a GPT? Visual intro to Transformers](https://www.youtube.com/watch?v=wjZofJX0v4M) | 3Blue1Brown 可视化讲解（1000万+播放） |
| 📺 YouTube | [Attention in transformers, visually explained](https://www.youtube.com/watch?v=eMlx5fFNoYc) | 3Blue1Brown 专注注意力机制 |
| 📺 B站 | [跟李沐学AI - Attention Is All You Need 论文精读](https://www.bilibili.com/video/BV1pu411o7BE) | 李沐论文精读，学术深度 |
