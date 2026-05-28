# GraphRAG 与高级 RAG

## 面试高频考点
- Naive RAG 的主要缺陷是什么？Advanced RAG 如何改进？
- GraphRAG 相比 RAG 解决了什么问题？核心流程是什么？
- HyDE 是什么？Self-RAG 如何判断是否需要检索？
- Chunk 切分策略如何选择？Embedding 模型如何选型？
- 如何评估 RAG 系统的质量？RAGAS 有哪些指标？

---

## RAG 演进三代

### 第一代：Naive RAG

```
用户 Query → 向量检索 → Top-K 文档 → Prompt 拼接 → LLM → 答案
```

**主要问题**：
- Chunk 切分粗糙，上下文割裂
- 单路向量检索召回率有限
- 检索噪声直接影响生成质量
- 无法处理多跳推理（答案需要跨多个文档关联）

### 第二代：Advanced RAG

在检索前后增加处理步骤：

```
┌──────────────────────────────────────────────────────┐
│ Pre-Retrieval（检索前优化）                            │
│  查询改写 → HyDE → 查询分解 → Step-Back Prompting     │
└──────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────┐
│ Retrieval（混合检索）                                  │
│  BM25（关键词）+ 向量检索（语义）→ RRF 融合            │
└──────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────┐
│ Post-Retrieval（检索后过滤）                           │
│  Reranker（Cross-Encoder 精排）→ 上下文压缩            │
└──────────────────────────────────────────────────────┘
```

### 第三代：GraphRAG / Agentic RAG

知识图谱 + Agent 自主规划，支持全局推理和多跳问题。

---

## 关键技术详解

### HyDE（假设文档嵌入）

**问题**：用户查询（短）和文档（长）在语义空间中分布差异大，直接匹配效果差。

**方案**：让 LLM 先生成一个"假设的理想答案文档"，用这个假设文档的 Embedding 去检索：

```
原始 Query: "什么是 RoPE 位置编码？"
         ↓ LLM 生成假设文档
假设文档: "RoPE（旋转位置编码）是一种通过旋转矩阵实现相对位置编码的方法，
          由苏剑林提出，被 LLaMA 等模型采用..."
         ↓ 用假设文档 Embedding 检索
真实文档库 → 找到真实的相关文档 → 拼接 Query + 文档 → LLM
```

**效果**：对"解释类"查询提升显著，检索召回率提升约 20-30%。

### Self-RAG（自反思 RAG）

模型自主决定**何时检索、检索什么、如何评估检索结果**，输出特殊 Reflection Token：

| Token 类型 | 含义 |
|-----------|------|
| `[Retrieve]` | 需要检索外部知识 |
| `[No Retrieve]` | 可基于参数知识直接回答 |
| `[Relevant]` | 检索内容与问题相关 |
| `[Irrelevant]` | 检索内容不相关，忽略 |
| `[Fully Supported]` | 生成内容完全有依据 |
| `[Partially Supported]` | 部分有依据 |

训练方式：特殊 Token 由 Critic LLM 标注，然后对 Generator LLM 做 SFT。

### 混合检索（Hybrid Retrieval）

| 检索方式 | 原理 | 适合场景 |
|---------|------|---------|
| BM25 | 词频-逆文档频率，关键词匹配 | 专有名词、精确查询 |
| 向量检索 | Embedding 语义相似度 | 语义相关、同义词、模糊查询 |
| **混合（RRF 融合）** | 两路结果排名倒数加权融合 | 大多数生产场景 |

```python
# Reciprocal Rank Fusion
def rrf_score(rank, k=60):
    return 1 / (k + rank)

score = rrf_score(bm25_rank) + rrf_score(vector_rank)
```

---

## GraphRAG（微软 2024）

**核心问题**：标准 RAG 无法回答需要跨文档全局综合的问题，如"这批文档的主要主题是什么？"

### 构建阶段（Indexing）

```
原始文档
   ↓ 文本切分
文本块（Chunks）
   ↓ LLM 抽取实体和关系
知识图谱（Entity + Relation）
   ↓ 社区检测（Louvain 算法）
层次社区结构（Communities）
   ↓ LLM 生成每个社区摘要
Community Reports
```

### 查询阶段（Query）

- **Local Search**：图谱 + 向量检索，适合精确实体查询，效果类似 Advanced RAG
- **Global Search**：跨所有社区摘要做 Map-Reduce 推理，适合全局综合类问题

**实测效果**：在全局理解类问题上比传统 RAG 提升 40%+，代价是索引成本高（需要大量 LLM 调用）。

---

## Chunk 策略

| 策略 | 方式 | 适用场景 |
|------|------|---------|
| 固定大小 | 按字符/Token 数切分 | 快速实现 |
| 句子切分 | NLTK/spaCy 按句子 | 逻辑完整 |
| 递归字符切分 | 按段落→句子→词 优先保留段落 | 通用文档（LangChain 默认）|
| 语义切分 | Embedding 相似度变化点切分 | 内容自适应 |
| 父文档检索 | 小 chunk 检索，返回大 chunk 上下文 | 精度 + 上下文平衡 |

**经验法则**：chunk_size 256-512 Token，overlap 50-100 Token，避免切断完整语义单元。

---

## RAG 评估（RAGAS 框架）

| 指标 | 衡量维度 | 计算方式 |
|------|---------|---------|
| **Faithfulness** | 答案是否有检索内容支撑 | 答案分解为原子事实，验证每条是否来自上下文 |
| **Answer Relevancy** | 答案是否回答了问题 | 用 LLM 从答案反推问题，与原问题计算相似度 |
| **Context Recall** | 检索内容是否覆盖了正确答案 | 与 Ground Truth 对比 |
| **Context Precision** | 检索内容中有用信息的比例 | 过滤噪声文档的能力 |

---

## 面试延伸

**Q：RAG 和 Long Context 长上下文，两者怎么选？**
> 长上下文（如 Gemini 1M Token）适合：知识库较小、需要精确引用、文档间关系重要；RAG 适合：知识库超大（几百万文档）、知识频繁更新、需要精确溯源（引用具体文档）、成本敏感（无需每次送入完整文档）。两者并非互斥，Agentic RAG 可以在长上下文窗口中动态检索。

**Q：Embedding 模型如何选型？**
> 中文：BGE 系列（BAAI）、M3E；英文：text-embedding-3-large（OpenAI）、E5-Large；多语言：mE5、BGE-M3。评估时用 MTEB 排行榜，重点看与业务场景最接近的任务类型（检索/分类/聚类）的得分，不要只看总分。

**Q：Reranker 为什么比向量检索精度更高？**
> 向量检索用 Bi-Encoder（Query 和文档独立 Encode），效率高但无法捕获 Query 和文档的交互特征。Reranker 用 Cross-Encoder（Query 和文档拼接后一起 Encode），可以精确建模交互，但无法预先计算文档 Embedding，只能对少量候选（Top-100）做精排，不能用于全量检索。

---

## 原始论文

| 论文 | 链接 |
|------|------|
| RAG 原始论文 (Lewis et al., 2020) | [arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401) |
| GraphRAG (Edge et al., Microsoft, 2024) | [arxiv.org/abs/2404.16130](https://arxiv.org/abs/2404.16130) |
| Self-RAG (Asai et al., 2023) | [arxiv.org/abs/2310.11511](https://arxiv.org/abs/2310.11511) |
| HyDE (Gao et al., 2022) | [arxiv.org/abs/2212.10496](https://arxiv.org/abs/2212.10496) |
| RAPTOR (Sarthi et al., 2024) | [arxiv.org/abs/2401.18059](https://arxiv.org/abs/2401.18059) |
| RAG Survey 2024 | [arxiv.org/abs/2312.10997](https://arxiv.org/abs/2312.10997) |
| LightRAG: Simple and Fast Graph-based RAG (2024) | [arxiv.org/abs/2410.05779](https://arxiv.org/abs/2410.05779) |
| HippoRAG: Neurobiologically Inspired Long-Term Memory (2024) | [arxiv.org/abs/2405.14831](https://arxiv.org/abs/2405.14831) |
| HippoRAG 2: From RAG to Memory (2025) | [arxiv.org/abs/2505.03842](https://arxiv.org/abs/2505.03842) |

## 延伸阅读与视频

| 平台 | 标题 | 说明 |
|------|------|------|
| 📺 B站 | [AI知识图谱GraphRAG是怎么回事？](https://www.bilibili.com/video/BV1Vf421X72h/) | 13万播放，B站最受欢迎的GraphRAG讲解 |
| 📺 B站 | [面试官：什么场景下必须用GraphRAG？而不是RAG？](https://www.bilibili.com/video/BV1vT421k7z9/) | 3.2万播放，场景选型角度讲透两者差异 |
| 📺 B站 | [15分钟跑通GraphRAG完整流程：从知识图谱构建到问答](https://www.bilibili.com/video/BV1Hm421x7ma/) | 6959播放，实战演示GraphRAG完整链路 |
| 📺 B站 | [使用Python构建RAG系统——用代码还原RAG系统的每个细节](https://www.bilibili.com/video/BV1sb421C7VD/) | 15万播放，代码级还原RAG系统实现 |
| 📺 B站 | [RAG优化：17种RAG方案，谁才是RAG最佳选择？](https://www.bilibili.com/video/BV1jT421q7qf/) | 1.1万播放，全面对比高级RAG改进方案 |
