# Transformer 架构详解

## 面试高频考点
- Transformer 整体结构是什么？
- Self-Attention 的计算过程？复杂度？
- 为什么要除以 sqrt(d_k)？
- Encoder-Decoder 和 Decoder-only 的区别？

---

## 整体架构

Transformer 由 **Encoder** 和 **Decoder** 两部分组成（原始论文），现代 LLM 普遍使用 **Decoder-only** 结构（GPT、LLaMA、Qwen 等）。

```
输入 → Embedding + 位置编码
     ↓
[× N 层]
  Multi-Head Self-Attention
  残差连接 + Layer Norm
  Feed-Forward Network
  残差连接 + Layer Norm
     ↓
输出层（Linear + Softmax）
```

---

## Self-Attention

**直觉**：每个 Token 去"询问"其他所有 Token 与自己的相关程度，加权聚合信息。

**计算步骤：**

1. 输入 X 经三个线性层得到 Q、K、V
2. 计算注意力分数：`scores = Q @ K^T / sqrt(d_k)`
3. Softmax 归一化：`weights = softmax(scores)`
4. 加权求和：`output = weights @ V`

```
Attention(Q, K, V) = softmax(QK^T / √d_k) · V
```

**为什么除以 sqrt(d_k)？**
> d_k 较大时，QK 点积方差随维度增大，导致 softmax 梯度极小（饱和区）。除以 sqrt(d_k) 将方差归一化，保持梯度稳定。

**时间复杂度**：O(n² · d)，n 为序列长度，这是长上下文的主要瓶颈。

---

## Multi-Head Attention

将 Q、K、V 分别投影到 h 个低维子空间，各自做 Attention，最后拼接再投影。

```python
# 每个头的维度 d_head = d_model / h
head_i = Attention(Q·W_i^Q, K·W_i^K, V·W_i^V)
MultiHead = Concat(head_1, ..., head_h) · W^O
```

**意义**：不同的头可以关注不同类型的依赖关系（句法、语义、位置等）。

---

## Causal Mask（因果掩码）

Decoder-only 模型生成时，每个位置只能看到自身及之前的 Token，通过在注意力分数上加上下三角 mask（将未来位置置为 -∞）实现。

---

## Feed-Forward Network（FFN）

每层 Attention 后接两层全连接：

```
FFN(x) = max(0, xW₁ + b₁)W₂ + b₂
```

现代模型多用 **SwiGLU** 激活替代 ReLU：

```
SwiGLU(x) = (xW₁) ⊙ σ(xW₁) · xW₂
```

FFN 的隐藏层维度通常是 d_model 的 4 倍，LLaMA 系列用 8/3 倍配合 SwiGLU。

---

## 残差连接 & Layer Norm

**残差连接**：`output = x + Sublayer(x)`，缓解梯度消失，允许堆叠更深的层。

**Pre-Norm vs Post-Norm：**
- Post-Norm（原始论文）：`LayerNorm(x + Sublayer(x))`，训练不稳定
- Pre-Norm（现代 LLM）：`x + Sublayer(LayerNorm(x))`，训练更稳定，可不预热

---

## Encoder-only / Decoder-only / Encoder-Decoder 对比

| 类型 | 代表模型 | 适用任务 |
|------|----------|----------|
| Encoder-only | BERT、RoBERTa | 分类、NER、语义匹配 |
| Decoder-only | GPT、LLaMA、Qwen | 文本生成、对话、推理 |
| Encoder-Decoder | T5、BART | 翻译、摘要、seq2seq |

---

## 面试延伸

**Q：为什么现代 LLM 都用 Decoder-only？**
> Decoder-only 用因果 Attention，预训练目标是下一个 Token 预测，天然适合生成任务，且在 scaling 时表现更好。

**Q：Attention 的 KV Cache 是怎么工作的？**
> 推理时每个新 Token 只需计算新的 Q，历史 Token 的 K、V 已缓存，无需重复计算。详见 [09_KV_Cache.md](./09_KV_Cache.md)。

**Q：Flash Attention 解决了什么问题？**
> 标准 Attention 需要把 n×n 的注意力矩阵写回 HBM（显存），IO 是瓶颈。Flash Attention 通过分块计算，将中间结果留在 SRAM，大幅减少显存读写。


---

## 原始论文

| 论文 | 链接 |
|------|------|
| Attention Is All You Need (Vaswani et al., 2017) | [arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762) |
| FlashAttention: Fast and Memory-Efficient Exact Attention (Dao et al., 2022) | [arxiv.org/abs/2205.14135](https://arxiv.org/abs/2205.14135) |

## 延伸阅读与视频

- 📺 **[But what is a GPT? Visual intro to Transformers](https://www.youtube.com/watch?v=wjZofJX0v4M)** — 3Blue1Brown，可视化讲解 Transformer（YouTube，1000万+播放）
- 📺 **[Attention in transformers, visually explained](https://www.youtube.com/watch?v=eMlx5fFNoYc)** — 3Blue1Brown，专注注意力机制（YouTube）
- 📺 **[跟李沐学AI - Attention Is All You Need 论文精读](https://www.bilibili.com/video/BV1pu411o7BE)** — Bilibili，李沐论文精读

> 欢迎 PR 补充更多优质资源
