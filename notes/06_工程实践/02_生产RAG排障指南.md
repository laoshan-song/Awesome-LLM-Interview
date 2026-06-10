# 生产 RAG 排障指南

## 面试高频考点

- RAG 答错了怎么定位？
- 如何区分检索问题和生成问题？
- 为什么看起来召回了文档，答案还是错？
- 如何设计 RAG 评估和线上反馈？
- 生产 RAG 常见失败模式有哪些？

---

## 外部图解：生产 RAG Pipeline

![NVIDIA：RAG ingest / query pipeline](https://developer-blogs.nvidia.com/wp-content/uploads/2023/12/rag-pipeline-ingest-query-flow-b.png)

> 图源：[NVIDIA Blog - RAG 101](https://developer.nvidia.com/blog/rag-101-demystifying-retrieval-augmented-generation-pipelines/)。这张图把离线 ingest 和在线 query 分开，适合定位 RAG 故障发生在哪一段。

---

## 一句话原则

RAG 排障不要直接怪模型，要按链路拆：

```text
问题理解 -> 检索召回 -> 排序 -> 上下文组装 -> 生成 -> 引用校验
```

每一层都有独立失败模式。

---

## 1. RAG 失败分类

| 失败类型 | 表现 | 主要原因 |
|------|------|----------|
| 没召回 | 正确文档不在 Top-K | chunk、embedding、query rewrite 问题 |
| 召回错 | Top-K 都是不相关文档 | 关键词歧义、权限过滤、索引污染 |
| 排序错 | 正确文档在后面 | 缺 rerank 或 rerank 模型不适配 |
| 上下文脏 | 太多噪声塞进 prompt | Top-K 太大、chunk 太长 |
| 生成错 | 证据正确但总结错 | prompt、模型能力、格式约束 |
| 引用错 | 答案和引用不匹配 | citation 绑定不严 |
| 不该答却答 | 证据不足仍然编 | 缺拒答策略和置信阈值 |

---

## 2. 排障流程

### Step 1：看正确文档有没有被召回

**排障细节：** 如果正确文档没有进入 Top-K，先不要调生成 prompt。应检查文档是否被接入、解析是否丢字段、chunk 是否切断答案、embedding 是否更新、权限过滤是否误杀、query 是否缺少关键词。这个阶段的目标是证明“证据能被找到”，否则后面 rerank 和生成都无从优化。

指标：

- Recall@5
- Recall@10

如果没召回：

- 检查 query 是否需要 rewrite
- 检查 chunk 是否切碎了关键信息
- 检查 embedding 是否适合语言和领域
- 检查关键词检索是否能补上专有名词

### Step 2：看正确文档排第几

指标：

- MRR
- NDCG

如果召回了但排后面：

- 加 reranker
- 用 RRF 融合 BM25 和向量检索
- 对标题、section_path 加权
- 针对业务术语做 query expansion

### Step 3：看上下文是否干净

指标：

- Context Precision
- 噪声 chunk 比例

如果上下文太脏：

- 降低 Top-K
- 缩短 chunk
- rerank 后再截断
- 对相同文档做去重

### Step 4：看生成是否忠于证据

**排障细节：** 如果证据已经正确进入上下文但答案仍错，要检查 prompt 是否要求引用、证据是否过长、多个证据是否冲突、关键证据是否排在中间或末尾、模型是否被系统指令或用户指令带偏。常见修复包括证据去重、把关键句提前、要求逐条引用、降低 temperature、增加拒答规则和使用更强模型处理最终生成。

指标：

- Faithfulness
- Citation Accuracy

如果证据对但答案错：

- prompt 强制“只基于证据”
- 加引用检查
- 不足时拒答
- 用更强模型生成
- 用 LLM-as-judge 做后验校验

---

## 3. Chunk 常见问题

### Chunk 太小

表现：

- 召回片段缺上下文
- 模型看不到完整条件
- 引用碎片化

解决：

- 增加 overlap
- 保留标题路径
- 按语义段落切

### Chunk 太大

表现：

- 召回不精准
- 上下文噪声多
- token 成本高

解决：

- 按标题、段落、表格单独切
- 对 FAQ 用问答对作为 chunk
- 对代码和日志单独策略

---

## 4. Query Rewrite 什么时候有用

适合：

- 用户问题太短
- 多轮对话有指代
- 问题抽象
- 需要拆多跳

不适合：

- 错误码
- 接口名
- 精确产品型号
- 日志关键字

规则：

> Rewrite 不能丢掉原始关键词。生产里通常原 query 和 rewrite query 一起检索。

---

## 5. Hybrid Search 为什么重要

向量检索擅长语义相似，但不擅长：

- 错误码
- 版本号
- API 名称
- 人名
- 产品编号
- 日志片段

BM25 擅长精确匹配，但不擅长同义改写。

所以生产默认建议：

```text
Dense Retrieval + BM25 + RRF + Rerank
```

---

## 6. 权限过滤怎么做

不要只在 prompt 里说“不能回答没权限内容”。

正确做法：

1. 检索前按租户、部门、标签过滤
2. 召回后再次过滤
3. 引用里只展示可见来源
4. 日志脱敏

如果权限过滤错了，RAG 会变成数据泄露系统。

---

## 7. 线上反馈闭环

日志至少记录：

- query
- rewritten query
- retrieved chunks
- rerank scores
- final context
- answer
- citations
- user feedback
- latency
- token cost

失败样本进入队列：

| 失败 | 处理 |
|------|------|
| 无答案 | 补知识库 |
| 召回错 | 调 chunk / embedding / hybrid |
| 生成错 | 改 prompt / 模型 / judge |
| 引用错 | 改 citation 绑定 |
| 用户不满意 | 标注偏好数据 |

---

## 常见误区

### 误区 1：Top-K 越大越好

Top-K 太大会引入噪声，让模型更容易答错。

### 误区 2：检索到了文档就不会幻觉

模型可能误读证据，也可能忽略证据。

### 误区 3：Embedding 换强模型一定解决问题

很多问题来自 chunk、权限、rerank 和 query rewrite。

### 误区 4：RAG 评估只看答案

必须把检索层和生成层拆开评估。

---

## 面试延伸

**Q：RAG 答错了你怎么排查？**

> 我会先看正确证据是否进入 Top-K，再看排序，再看上下文噪声，最后看生成是否忠于证据。对应指标是 Recall@K、MRR、Context Precision、Faithfulness 和 Citation Accuracy。

**Q：为什么 Hybrid Search 比纯向量检索稳？**

> 因为企业问题里有大量错误码、接口名、版本号和专有名词，BM25 对这些更稳；向量检索补语义改写，两者融合能提高召回鲁棒性。

**Q：如何避免 RAG 泄露无权限文档？**

> 权限必须在检索系统层实现，按租户和标签过滤，不能只靠 prompt 约束模型。

---

## 生产排障 Runbook

线上 RAG 出错时，建议按固定 runbook 处理，而不是临时猜：

```text
1. 复现 query，固定用户身份和权限
2. 查看 rewrite query
3. 查看 dense / BM25 各自 Top-K
4. 查看 fusion 和 rerank 后排序
5. 查看 ACL filter 前后数量
6. 查看最终 prompt 中的 context
7. 查看模型答案是否忠于证据
8. 给失败打标签，进入优化队列
```

失败标签建议：

| 标签 | 含义 | 处理 |
|------|------|------|
| knowledge_missing | 知识库没有答案 | 补文档、补 FAQ |
| parse_failed | 文档解析失败 | 修解析器、表格/OCR |
| chunk_bad | chunk 切分不合理 | 改 chunk 策略 |
| retrieval_miss | 正确证据没召回 | 调 embedding/BM25/rewrite |
| rerank_bad | 召回了但排序靠后 | 调 reranker 或训练数据 |
| context_noise | 上下文噪声太多 | 降 Top-K、压缩证据 |
| generation_unfaithful | 模型没按证据答 | 改 prompt、加引用校验 |
| acl_error | 权限过滤错误 | 修 metadata 和 filter |

---

## RAG 评估集怎么构建

生产 RAG 的评估集不应该只有“问题-答案”，最好包含证据：

```json
{
  "question": "模型 API 超时怎么排查？",
  "gold_answer": "...",
  "gold_chunk_ids": ["ops_001", "gateway_014"],
  "must_cite": true,
  "tenant": "internal",
  "difficulty": "multi-hop"
}
```

评估维度：

- **Retrieval Recall@K**：gold chunk 是否被召回。
- **MRR/NDCG**：正确证据排序是否靠前。
- **Faithfulness**：答案是否被证据支持。
- **Citation Accuracy**：引用是否真实对应答案。
- **Refusal Accuracy**：无证据或无权限时是否拒答。
- **Latency/Cost**：质量提升是否值得成本。

---

## 面试回答模板

如果被问“RAG 线上效果差怎么办”，可以这样回答：

> 我不会先改模型，而是先拆链路。第一看正确证据在不在知识库，第二看有没有被 dense/BM25 召回，第三看 fusion/rerank 后有没有进入上下文，第四看模型是否忠于证据。每层都有对应指标和日志，定位后再决定补文档、调 chunk、换 embedding、加 rerank、改 prompt 或做权限修复。

这个回答能体现你理解 RAG 是系统工程，而不是一个向量库 demo。

---

## 原始论文

| 论文 | 链接 |
|------|------|
| Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (Lewis et al., 2020) | [arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401) |
| Dense Passage Retrieval for Open-Domain Question Answering (Karpukhin et al., 2020) | [arxiv.org/abs/2004.04906](https://arxiv.org/abs/2004.04906) |
| Self-RAG: Learning to Retrieve, Generate, and Critique (Asai et al., 2023) | [arxiv.org/abs/2310.11511](https://arxiv.org/abs/2310.11511) |
| Corrective RAG (Yan et al., 2024) | [arxiv.org/abs/2401.15884](https://arxiv.org/abs/2401.15884) |
| RAGAS: Automated Evaluation of Retrieval Augmented Generation (Es et al., 2023) | [arxiv.org/abs/2309.15217](https://arxiv.org/abs/2309.15217) |

## 延伸阅读与视频

| 平台 | 标题 | 说明 |
|------|------|------|
| 📖 NVIDIA Blog | [RAG 101: Demystifying Retrieval-Augmented Generation Pipelines](https://developer.nvidia.com/blog/rag-101-demystifying-retrieval-augmented-generation-pipelines/) | 生产 RAG pipeline 的工程拆解 |
| 📖 LangChain Docs | [RAG evaluation concepts](https://docs.smith.langchain.com/evaluation) | 线上 trace 和 RAG 评估入口 |
| 📖 LlamaIndex Docs | [Evaluating RAG applications](https://docs.llamaindex.ai/en/stable/understanding/evaluating/evaluating/) | RAG 检索和生成评估实践 |
| 📖 Anthropic Research | [Prompt injection defenses](https://www.anthropic.com/research/prompt-injection-defenses) | RAG/Agent 场景下的提示注入风险 |
