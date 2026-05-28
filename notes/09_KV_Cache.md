# KV Cache 原理与优化

## 面试高频考点
- KV Cache 是什么？解决了什么问题？
- KV Cache 的显存占用如何计算？
- PagedAttention 的思路？

---

## 为什么需要 KV Cache？

自回归生成时，每生成一个新 Token，标准做法需要对所有历史 Token 重新计算 Attention。

**KV Cache**：缓存每一层每个历史 Token 的 K、V，新 Token 只需计算自己的 Q、K、V，然后与缓存拼接。

计算量从 O(n²) 降至每步 O(n)（n 为当前序列长度）。

---

## KV Cache 显存占用

```
显存 = 2 × num_layers × num_kv_heads × head_dim × seq_len × batch_size × dtype_bytes
```

以 LLaMA-2 70B（80层，GQA 8组，head_dim=128，FP16，seq_len=4096）为例：
```
2 × 80 × 8 × 128 × 4096 × 1 × 2 bytes ≈ 40GB
```

KV Cache 的显存占用往往和模型权重本身相当，是推理的核心瓶颈。

---

## GQA（分组查询注意力）

**MHA**：每个头独立 KV，KV Cache 最大。
**MQA**：所有 Query 头共享一组 KV，KV Cache 减少 h 倍，质量略降。
**GQA**：G 组 Query 头共享一组 KV，折中方案。

| 方式 | KV 组数 | 代表模型 |
|------|---------|----------|
| MHA | = num_heads | GPT-2、BERT |
| MQA | 1 | 早期 PaLM |
| GQA | num_heads / G | LLaMA 2 70B、Qwen |

---

## PagedAttention（vLLM）

**问题**：传统框架为每个请求预分配固定长度 KV Cache，导致大量显存碎片和浪费（利用率 < 40%）。

**PagedAttention**：借鉴操作系统分页机制，KV Cache 存储在不连续的物理 Block 中，通过 Block Table 映射。

**效果**：显存利用率提升至 90%+，吞吐量大幅提升。

---

## 其他 KV Cache 优化

| 技术 | 思路 |
|------|------|
| KV Cache 量化 | INT8/FP8 存储，节省一半显存 |
| Sliding Window | 只保留最近 W 个 Token 的 KV |
| Prefix Caching | 相同 System Prompt 的 KV 跨请求共享 |
| StreamingLLM | 保留开头 attention sink + 滑动窗口 |

---

## 面试延伸

**Q：Prefill 和 Decode 阶段的区别？**
> Prefill：对输入 Prompt 并行计算，生成初始 KV Cache，计算密集（compute-bound）。Decode：逐 Token 自回归生成，访存密集（memory-bound）。

**Q：为什么 Decode 阶段是 memory-bound？**
> 每步只处理一个 Token，计算量极小，但需要从显存加载全部模型权重和 KV Cache，带宽成为瓶颈。


---

## 原始论文

| 论文 | 链接 |
|------|------|
| Efficient Memory Management for LLM Serving with PagedAttention (Kwon et al., 2023) | [arxiv.org/abs/2309.06180](https://arxiv.org/abs/2309.06180) |
| GQA: Training Generalized Multi-Query Transformer Models (Ainslie et al., 2023) | [arxiv.org/abs/2305.13245](https://arxiv.org/abs/2305.13245) |

## 延伸阅读与视频

- 📺 **[Bilibili 搜索"KV Cache 推理加速"](https://search.bilibili.com/all?keyword=KV+Cache%E6%8E%A8%E7%90%86%E5%8A%A0%E9%80%9F&order=click)** — 按播放量筛选
- 📺 **[YouTube 搜索"KV Cache LLM explained"](https://www.youtube.com/results?search_query=KV+cache+LLM+explained)** — 按播放量筛选

> 欢迎 PR 补充更多优质资源
