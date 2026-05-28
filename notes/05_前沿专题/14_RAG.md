# RAG（检索增强生成）

## 面试高频考点
- RAG 的基本流程是什么？每步的关键设计选择？
- 向量检索和关键词检索的区别？何时用混合检索？
- 如何评估 RAG 系统的效果？
- RAG vs Fine-tuning vs 长上下文？
- 高级 RAG 技术有哪些？

---

## 一、为什么需要 RAG？

LLM 存在固有局限，RAG 通过**检索→增强→生成**的范式在推理时注入外部知识：

| LLM 的局限 | RAG 如何解决 |
|-----------|-------------|
| 知识截止日期 | 知识库实时更新，检索到最新信息 |
| 幻觉（编造事实） | 生成受检索到的真实文档约束 |
| 无法访问私有数据 | 企业知识库/文档库作为检索源 |
| 不可验证（无引用） | 可追溯每个回答的依据来源 |
| 长尾知识覆盖不足 | 知识库可无限扩展，不受模型参数限制 |

---

## 二、RAG 完整链路

```
┌──────────────────────────────────────────────────────┐
│                  RAG 完整流水线                        │
│                                                       │
│  离线阶段（Indexing）：                                 │
│    文档 → 解析 → 分块 → Embedding → 向量数据库建索引     │
│                                                       │
│  在线阶段（Querying）：                                 │
│    用户问题                                           │
│      ↓                                               │
│  ① Query 改写（可选）：扩写指代、补全上下文              │
│      ↓                                               │
│  ② 检索（Retrieval）：从向量数据库召回 Top-K           │
│      ↓                                               │
│  ③ 重排（Re-ranking）：Cross-Encoder 精排              │
│      ↓                                               │
│  ④ 上下文组装：将检索片段拼入 Prompt                   │
│      ↓                                               │
│  ⑤ 生成（Generation）：LLM 基于上下文回答              │
│      ↓                                               │
│  ⑥ 引用/验证（可选）：标注来源、检查忠实度              │
└──────────────────────────────────────────────────────┘
```

### 每一步的关键设计选择

| 步骤 | 选择 1 | 选择 2 | 决策依据 |
|------|--------|--------|---------|
| Chunking | 固定大小 512 tokens | 语义分块 | 文档类型 |
| Embedding | text-embedding-3 (OpenAI) | BGE-M3 (开源) | 成本/精度/多语言 |
| 向量库 | Milvus (分布式) | Qdrant (高性能) | 数据规模/QPS |
| 检索策略 | 纯向量 | Hybrid (BM25+向量) | 是否需要精确关键词匹配 |
| Re-ranker | Cohere Rerank (SaaS) | BGE-Reranker (开源) | 成本/延迟 |
| LLM | GPT-4 (SaaS) | DeepSeek-V3 (开源) | 成本/质量/合规 |

---

## 三、检索方式详解

### 三种检索方式对比

```
稠密检索（Dense Retrieval）：
  "便宜的笔记本电脑" → Embedding → [0.23, -0.45, 0.78, ...]
  在向量空间中搜索最近邻
  匹配："性价比高的笔记本"、"实惠的电脑"、"便宜本推荐"
  优势：理解语义改写，同义词匹配
  短板：数字/代码/专有名词匹配不精确

稀疏检索（Sparse / BM25）：
  "便宜的笔记本电脑" → 分词 → {"便宜":1, "笔记本":1, "电脑":1}
  基于 TF-IDF/BM25 计算匹配分数
  匹配：包含"便宜"、"笔记本"、"电脑"的文档
  优势：精确关键词匹配，速度快，可解释
  短板：不理解"性价比高"=便宜

混合检索（Hybrid Search）：
  Dense Score: 0.82, BM25 Score: 0.65
  融合：RRF(0.82, 0.65) → 综合排名
  优势：语义 + 关键词互补，召回率最高
  代价：需要维护两套索引，融合策略需调优
```

### 分数融合：RRF（Reciprocal Rank Fusion）

```
最简单的融合方式，无需调权重：

RRF_score = Σ 1/(k + rank_d)

其中 k 是常数（通常 60），rank_d 是该文档在第 d 个检索器中的排名

例子：
  文档 A：Dense 排第 2，BM25 排第 5
  RRF = 1/(60+2) + 1/(60+5) = 0.0161 + 0.0154 = 0.0315

  文档 B：Dense 排第 5，BM25 排第 1
  RRF = 1/(60+5) + 1/(60+1) = 0.0154 + 0.0164 = 0.0318  ← B 略高
```

---

## 四、Query 改写技术

原始用户问题往往不适合直接检索，需要改写：

| 技术 | 做法 | 示例 |
|------|------|------|
| **HyDE** | 让 LLM 先生成假设答案，用假答案去检索 | 问题："什么是KV Cache" → 生成假答案 → 用假答案检索 |
| **Multi-Query** | 同一问题生成 3-5 个不同表述，分别检索后合并 | "LLM 幻觉怎么解决" → 生成 "减少AI编造" "提高事实准确性" 变体 |
| **Step-back** | 回溯到更抽象/基础的问题 | "2024年A100相比H100的性价比" → step-back "GPU性能对比方法" |
| **Query Decomposition** | 把复杂问题拆成子问题，分别检索 | "对比BERT和GPT在情感分析上的表现" → "BERT情感分析" + "GPT情感分析" |
| **Contextual Rephrasing** | 结合对话历史改写指代不明的问题 | 历史："什么是Transformer" 当前："它的复杂度呢" → 改写为"Transformer的复杂度" |

---

## 五、RAG 的评估

### RAGAS（RAG Assessment）框架

| 指标 | 衡量什么 | 计算方式 |
|------|---------|---------|
| **Faithfulness（忠实度）** | 生成答案是否忠于检索到的上下文 | 提取答案中的事实声明 → 检查每个声明是否被上下文支持 |
| **Answer Relevance** | 答案与问题的相关度 | 用答案反向生成问题 → 检查与原问题的语义相似度 |
| **Context Precision** | 检索结果中相关文档的排名是否靠前 | 相关文档在 Top-K 中的位置加权 |
| **Context Recall** | 检索结果覆盖了多少 ground truth 信息 | 标注关键信息点 → 检查检索结果覆盖了哪些 |

### 端到端指标

```
检索阶段：
  - Recall@K：相关文档在 Top-K 中的比例
  - MRR (Mean Reciprocal Rank)：第一个相关文档的排名倒数
  - NDCG@K：考虑排名位置的相关性加权

生成阶段：
  - 忠实度（基于 NLI 或 LLM-as-Judge）
  - 答案正确性（对比标注答案）
  - 引用准确率（引用的来源是否一致）
```

---

## 六、高级 RAG 技术

### Self-RAG

模型在生成过程中**自我判断**是否需要检索、检索到的内容是否有用：

```
对每个生成段：
  ① Retrieve Token：决定"是否需要检索更多信息？"
  ② Critique Token：评估检索片段"是否相关/有用/准确？"
  ③ 基于评估结果：使用、忽略、或重新检索

比标准 RAG 更灵活，不会强行使用不相关的检索结果
```

### Corrective RAG（CRAG）

对检索结果做"质量检查"→ 如果质量不够，自动触发纠错：

```
检索 Top-K → 评估相关性分数 →
  如果分数 > 阈值 → 直接使用
  如果分数中等 → 补充 Web Search
  如果分数 < 阈值 → 丢弃，仅用 Web Search 结果
```

### Agentic RAG

将 RAG 嵌入 Agent 框架中，LLM 自主决定检索策略：

```
Agent 可以：
  - 自主选择检索哪些知识库
  - 根据部分结果调整后续查询
  - 多轮检索 + 交叉验证
  - 结合不同来源的信息（文档+数据库+API）
```

---

## 七、RAG vs 长上下文 vs Fine-tuning

| 维度 | RAG | 长上下文 LLM | Fine-tuning |
|------|-----|-------------|-------------|
| 知识更新 | 实时（改知识库即可） | 需重训或依赖窗口 | 需重新微调 |
| 事实准确性 | 高（引用明确来源） | 中（hallucination仍存在） | 低（内化为参数，难以验证） |
| 推理成本 | 检索成本 + LLM 推理 | 仅 LLM 推理（但长上下文贵） | 仅 LLM 推理 |
| 适用数据量 | 海量（TB级知识库） | 受窗口限制 | 受训练数据限制 |
| 引用可追溯 | ✅ | ❌ | ❌ |
| 延迟 | 中（检索耗时） | 低 | 低 |
| 最佳场景 | 知识密集、需溯源 | 单文档深度分析 | 风格/行为学习 |

**综合推荐**：知识密集型（客服/法律/医疗）→ RAG；深度单文档分析 → 长上下文；风格迁移/特定行为 → Fine-tuning；生产系统常三者结合。

---

## 八、面试延伸

**Q：如何评估 RAG 系统？从哪些维度看？**

> 检索维度（Recall@K, MRR, NDCG）和生成维度（忠实度、答案相关性、正确性）。RAGAS 是常用的自动化评估框架，通过 LLM-as-Judge 自动打分。完整的评估 pipeline 需要人工标注 Ground Truth 数据集（包含正确的检索文档和正确答案）。

**Q：RAG 和 Fine-tuning 如何选择？可以结合吗？**

> RAG 适合知识频繁更新的场景、需要引用来源的场景；Fine-tuning 适合改变模型输出风格和学习固定领域知识。可以结合：先用 Fine-tuning 让模型学会特定领域的术语和推理方式，再用 RAG 提供实时事实。这是目前许多企业落地的主流方案。

**Q：RAG 为什么仍然会产生幻觉？如何缓解？**

> 主要原因：检索不到（召回失败）、检索到错误信息（检索错）、上下文过长模型忽略证据（lost in the middle）、多个证据冲突。缓解：提升检索质量（Hybrid、Query Rewrite）、Reranker 精排、在 Prompt 中强制引用来源、设置"无证据时拒答"机制、对关键事实做二次验证。

---

## 原始论文

| 论文 | 链接 |
|------|------|
| RAG: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (Lewis et al., NeurIPS 2020) | [arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401) |
| Self-RAG: Learning to Retrieve, Generate, and Critique (Asai et al., ICLR 2024) | [arxiv.org/abs/2310.11511](https://arxiv.org/abs/2310.11511) |
| Corrective RAG (CRAG) (Yan et al., 2024) | [arxiv.org/abs/2401.15884](https://arxiv.org/abs/2401.15884) |
| RAGAS: Automated Evaluation of RAG (Es et al., 2024) | [arxiv.org/abs/2309.15217](https://arxiv.org/abs/2309.15217) |
| HyDE: Precise Zero-Shot Dense Retrieval without Relevance Labels (Gao et al., 2023) | [arxiv.org/abs/2212.10496](https://arxiv.org/abs/2212.10496) |

## 延伸阅读与视频

| 平台 | 标题 | 说明 |
|------|------|------|
| 📺 YouTube | [Retrieval Augmented Generation (RAG) Explained](https://www.youtube.com/watch?v=T-D1OfcDW1M) | IBM Technology，百万播放，清晰入门 |
| 📺 B站 | [Bilibili 搜索"RAG 检索增强生成"](https://search.bilibili.com/all?keyword=RAG%E6%A3%80%E7%B4%A2%E5%A2%9E%E5%BC%BA%E7%94%9F%E6%88%90&order=click) | 按播放量筛选中文讲解 |
