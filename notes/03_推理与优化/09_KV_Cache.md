# KV Cache 原理与优化

## 面试高频考点
- KV Cache 是什么？解决了什么问题？
- KV Cache 的显存占用如何计算？
- PagedAttention 的思路？
- GQA / MQA 为什么能减少 KV Cache？
- Prefill 和 Decode 的区别？

---

## 一、为什么需要 KV Cache？

### 自回归生成的问题

LLM 逐 token 生成时，每生成一个新 token，传统做法需要对**所有历史 token** 重新计算 Attention。这意味着：

- 生成第 1 个 token：算 1 个 token 的 Attention
- 生成第 2 个 token：算 2 个 token 的 Attention
- 生成第 n 个 token：算 n 个 token 的 Attention

总计算量 = 1 + 2 + 3 + ... + n = O(n²)，非常浪费。

### KV Cache 的核心思想

Attention 计算中，已生成 token 的 Key 和 Value 在后续步骤中**不会改变**（因果掩码保证当前 token 看不到未来）：

```
Step 1: 生成 "我" → 计算 K₁,V₁ 并缓存
Step 2: 生成 "爱" → 重用 K₁,V₁，只算 Q₂,K₂,V₂ → 缓存 K₂,V₂
Step 3: 生成 "你" → 重用 K₁,V₁,K₂,V₂，只算 Q₃,K₃,V₃ → 缓存 K₃,V₃
...

每步只计算 1 个新 token 的 Q,K,V，将新 K,V 追加到缓存中。
```

**效果**：每步计算量从 O(n²·d) 降至 O(n·d)，推理速度大幅提升。

```
        ┌─────────────────────────────────────┐
        │          KV Cache 示意图              │
        │                                      │
        │  时间步 →                            │
        │                                      │
        │  t=1: [K₁V₁]                        │
        │  t=2: [K₁V₁][K₂V₂]                  │
        │  t=3: [K₁V₁][K₂V₂][K₃V₃]            │
        │  t=4: [K₁V₁][K₂V₂][K₃V₃][K₄V₄]      │
        │                                      │
        │  每步新计算的 Q_t 与所有历史 K 做点积    │
        │  Q₄ · [K₁ K₂ K₃ K₄] → softmax → × V  │
        └─────────────────────────────────────┘
```

### 为什么只缓存 K 和 V，而不缓存 Q？

Q（Query）只用于当前 token 查询历史信息，后续 token 不需要之前 token 的 Q。而 K（Key）和 V（Value）需要被未来的 token 查询和聚合。

---

## 二、KV Cache 显存计算

### 公式

```
KV Cache 大小 = 2 × n_layers × n_kv_heads × d_head × seq_len × batch_size × dtype_bytes
```

其中 `2` 代表 K 和 V 各一份。

### 逐层推导

以 **LLaMA-2 7B**（FP16，batch=1，seq_len=4096）为例：

| 参数 | 值 | 说明 |
|------|-----|------|
| n_layers | 32 | Transformer 层数 |
| n_kv_heads | 32（MHA 模式）| KV 头数，GQA 下更少 |
| d_head | 128 | 每头维度 |
| seq_len | 4096 | 序列长度 |
| dtype_bytes | 2 | FP16 = 2 bytes |

```
KV Cache = 2 × 32 × 32 × 128 × 4096 × 1 × 2 bytes
         = 2 × 32 × 32 × 128 × 4096 × 2
         = 2,147,483,648 bytes ≈ 2 GB
```

### 不同模型的 KV Cache 对比

| 模型 | 参数量 | KV 头数 | seq_len=4096 FP16 | seq_len=128K FP16 |
|------|--------|---------|-------------------|--------------------|
| LLaMA-2 7B (MHA) | 7B | 32 | ~2 GB | ~64 GB |
| LLaMA-2 70B (GQA) | 70B | 8 | ~1 GB | ~33 GB |
| Mistral 7B (GQA) | 7B | 8 | ~0.5 GB | ~16 GB |

**关键发现**：长上下文场景下，KV Cache 显存可远超模型权重本身（70B 模型权重 ~140GB，128K 序列单个 batch 的 KV Cache 就 33GB）。

### GQA 如何减少 KV Cache

```
MHA（Multi-Head Attention）:
  Q₁ Q₂ Q₃ Q₄ → 各自对应独立的 K₁/V₁, K₂/V₂, K₃/V₃, K₄/V₄
  KV 份数 = 头数 h

GQA（Grouped-Query Attention, G=4）:
  Q₁ Q₂ → 共享 K₁/V₁
  Q₃ Q₄ → 共享 K₂/V₂
  KV 份数 = h/G

MQA（Multi-Query Attention）:
  Q₁ Q₂ Q₃ Q₄ → 全部共享同一组 K/V
  KV 份数 = 1
```

**GQA 节省比例 = h / G**。例如 LLaMA-2 70B 用 GQA with 8 KV heads（共 64 个 Q heads），KV Cache 减少 8 倍。

---

## 三、Prefill 与 Decode 阶段

### 两个阶段对比

```
┌──────────────────────────────────────────────────────┐
│                   推理两个阶段                         │
├──────────────────────┬───────────────────────────────┤
│   Prefill (预填充)     │   Decode (解码)               │
├──────────────────────┼───────────────────────────────┤
│ 输入：整个 prompt      │ 输入：上一时刻生成的 1 个 token │
│ 计算：并行处理所有 token │ 计算：只算当前 token + KV Cache │
│ 瓶颈：Compute-Bound   │ 瓶颈：Memory-Bound            │
│ GPU 算力受限           │ 显存带宽受限                   │
│ 产出：初始 KV Cache    │ 产出：逐 token 追加到 KV Cache │
└──────────────────────┴───────────────────────────────┘
```

### 为什么 Decode 是 Memory-Bound？

每次 Decode 步只处理 **1 个 token**，计算量极小（约 2 × 参数量 FLOPs），但需要：

1. 从显存加载**全部模型权重**（7B 模型 = 14GB FP16）
2. 从显存加载**全部 KV Cache**
3. 每次只做极少的矩阵乘法

**类比**：从仓库（显存）运一卡车货物（权重），只为了加工一个小零件（1 token）。大部分时间在运输，不在加工。

### 分离式 Prefill/Decode（Disaggregated P/D）

```
        ┌─────────────┐    KV Cache     ┌─────────────┐
用户 ──→│ Prefill 集群 │ ──────────────→ │ Decode 集群  │──→ 输出
        │ 高算力 GPU   │    (网络传输)    │ 大显存 GPU   │
        └─────────────┘                  └─────────────┘

优势：
- Prefill 用 H100（高算力），Decode 用大显存卡
- 两个阶段独立扩缩容
- 整体吞吐提升 40%+
```

---

## 四、PagedAttention 详解

### 传统 KV Cache 的问题

```
传统方案：为每个请求预分配连续的最大长度空间

请求 A（max_len=2048）: [████████░░░░░░░░░░░░]  浪费 50%
请求 B（max_len=4096）: [███░░░░░░░░░░░░░░░░░]  浪费 85%
请求 C（max_len=1024）: [████████████████████]  浪费 0%

内部碎片 + 外部碎片 → 总利用率 < 40%
```

### PagedAttention 方案

将 KV Cache 切成固定大小的 **Block**（如 16 token/block），通过 **Block Table** 映射：

```
物理 Block 池:
┌────┬────┬────┬────┬────┬────┬────┬────┐
│ B0 │ B1 │ B2 │ B3 │ B4 │ B5 │ B6 │ B7 │  ← 按需分配
└────┴────┴────┴────┴────┴────┴────┴────┘
  ↓    ↓    ↓    ↓         ↓    ↓
 请求A  请求A  请求B  请求B   请求C  请求A (追加)

请求 A 的 Block Table: [B0, B1, B7]      ← 不连续物理块，逻辑连续
请求 B 的 Block Table: [B2, B3]
请求 C 的 Block Table: [B5]
```

**Copy-on-Write 实现 Prefix Sharing**：

```
请求 A: system_prompt = "你是一个..."  → Block [B0, B1]
请求 B: system_prompt = "你是一个..."  → 共享 Block [B0, B1]（只读，不复制）

只有当某个请求修改了共享 Block 中的内容时，才触发复制。
对于推理场景（KV Cache 只追加不修改），大量请求可共享相同 system prompt 的 KV Cache。
```

### PagedAttention 的效果

| 指标 | 传统方案 | PagedAttention |
|------|---------|----------------|
| 显存利用率 | < 40% | > 90% |
| 内存碎片 | 严重 | 几乎无 |
| Prefix Sharing | 不支持 | 原生支持 |
| 吞吐量 | 基线 | 2-4x 提升 |

---

## 五、其他 KV Cache 优化技术

### 1. KV Cache 量化（KVQuant / KIVI）

```
不量化权重，只量化 KV Cache：
- K 和 V 以 FP16 计算，存储时压缩为 INT8/INT4
- 读取时解压回 FP16 参与 Attention 计算
- 关键：K 的分布通常不均匀（有 outlier 通道），需要 per-channel 量化
- 可节省 50-75% 的 KV Cache 显存
```

### 2. Sliding Window Attention（Mistral 风格）

```
只保留最近 W 个 token 的 KV Cache，丢弃更早的：

[丢弃] [丢弃] [保留 W=4096]

优点：KV Cache 大小恒定 O(W)，不随序列增长
缺点：丢失长距离依赖（对某些任务不适用）
```

### 3. StreamingLLM（Attention Sink）

```
发现：前几个 token（"attention sink"）对模型稳定性至关重要

StreamingLLM 策略：
[保留前 4 个 token] + [滑动窗口最近 W 个 token]

即使超过窗口长度，保留开头几个 token 就能维持模型性能
```

### 4. Prefix Caching

```
多个请求共享相同的 system prompt 时：

请求 1 system: "你是一个专业的代码助手..." → 计算一次 KV
请求 2 system: "你是一个专业的代码助手..." → 复用！跳过计算
请求 3 system: "你是一个专业的代码助手..." → 复用！跳过计算

vLLM 和 SGLang 均原生支持。适合聊天应用（system prompt 固定）。
```

### 5. Multi-Query / Grouped-Query Attention

| 方案 | KV 份数 | KV Cache | 质量 |
|------|---------|----------|------|
| MHA | h | 最大 | 最好 |
| GQA | h/G | 中等 | 极轻微损失 |
| MQA | 1 | 最小 | 有轻微损失 |

**当前主流**：GQA（LLaMA 2/3、Mistral、Qwen 均采用），在质量和效率间取得最佳平衡。

---

## 六、面试延伸

**Q：KV Cache 在推理时占多少显存？如何估算？**

> 公式：`2 × n_layers × n_kv_heads × d_head × seq_len × batch_size × dtype_bytes`
>
> 以 LLaMA-2 13B（40层, 40头, d_head=128, FP16, batch=8, seq_len=2048）为例：
> `2 × 40 × 40 × 128 × 2048 × 8 × 2 ≈ 13.4 GB`
>
> 13B 模型权重约 26GB，KV Cache 占了 13.4GB，总计约 40GB，需要 A100（40GB/80GB）才能跑 batch=8。

**Q：Prefill 和 Decode 的瓶颈不同，实际如何优化？**

> Prefill（compute-bound）：增大 batch 提高 GPU 算力利用率；用 FP8 加速矩阵运算；Chunked Prefill 将长 prompt 分块与 decode 交错执行。
>
> Decode（memory-bound）：减少需要从显存读的数据量——GQA 减少 KV 头数、KV Cache INT8 量化压缩存储、PagedAttention 减少浪费。
>
> 最新方向：Disaggregated Prefill/Decode，将两个阶段部署在不同硬件上独立优化。

**Q：GQA 为什么几乎不损失精度？**

> 不同 Q 头关注不同的语义模式（句法、语义、位置等），但它们查询的 K/V 空间高度重叠。实验表明共享 K/V 对多数任务影响极小（< 0.5%），而 KV Cache 节省显著。GQA 在 MHA 和 MQA 之间取得了实用平衡。

**Q：PagedAttention 的 Block Size 如何选择？**

> Block size 越大，Block Table 越小，管理开销低，但内存碎片增多。Block size 越小，内存利用率越高，但 Block Table 变大。vLLM 默认 block_size=16（tokens），经过实验验证是较好的平衡点。对于超长序列（128K+），可适当增大到 32-64。

---

## 补充：FlashAttention 与 KV Cache 的关系

FlashAttention 本身是 Attention 计算的 IO 优化（减少 HBM 读写），但它和 KV Cache 有协同效应：

- **FlashAttention**：让每次 Attention 计算更快、更省显存
- **PagedAttention / KV Cache**：让多次 Attention 计算复用中间结果

两者结合（vLLM 的做法）能获得最大的推理加速：计算快 + 少重复计算 + 显存高效管理。

---

## 原始论文

| 论文 | 链接 |
|------|------|
| Efficient Memory Management for LLM Serving with PagedAttention (Kwon et al., SOSP 2023) | [arxiv.org/abs/2309.06180](https://arxiv.org/abs/2309.06180) |
| GQA: Training Generalized Multi-Query Transformer Models (Ainslie et al., 2023) | [arxiv.org/abs/2305.13245](https://arxiv.org/abs/2305.13245) |
| FlashAttention: Fast and Memory-Efficient Exact Attention (Dao et al., NeurIPS 2022) | [arxiv.org/abs/2205.14135](https://arxiv.org/abs/2205.14135) |
| StreamingLLM: Efficient Streaming Language Models with Attention Sink (Xiao et al., 2023) | [arxiv.org/abs/2309.17453](https://arxiv.org/abs/2309.17453) |
| KVQuant: Towards 10 Million Context Length (Hooper et al., 2024) | [arxiv.org/abs/2401.18079](https://arxiv.org/abs/2401.18079) |
| Mooncake: KVCache-centric Disaggregated Architecture (Qin et al., 2024) | [arxiv.org/abs/2407.00079](https://arxiv.org/abs/2407.00079) |

## 延伸阅读与视频

| 平台 | 标题 | 说明 |
|------|------|------|
| 📺 B站 | [vLLM PagedAttention 论文精读](https://www.bilibili.com/video/BV1GWjjzfE1b/) | 近2小时完整解读 PagedAttention 论文 |
| 📺 B站 | [怎么加快大模型推理？10分钟学懂vLLM内部原理](https://www.bilibili.com/video/BV1kx4y1x7bu/) | 12.4万播放，最受欢迎的 vLLM+PagedAttention 讲解 |
