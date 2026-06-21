# 23-大模型（LLMs）RAG —— 关键痛点及对应解决方案

> 来源 PDF：`200页AI大模型面试高频必刷题（附详解）/23-大模型（LLMs）RAG —— 关键痛点及对应解决方案.pdf`  
> 主题：RAG / 文档问答  
> 页数：15  
> 字符数：16978  
> 索引片段数：42

## 摘要

大模型（LLMs）RAG —— 关键痛点及对应解决方案 来自： AiGC面试宝典 宁静致远 2024年03月19日 22:30 • 大模型（LLMs）RAG —— 关键痛点及对应解决方案 • 前言 • 问题一：内容缺失问题 • 1.1 介绍一下 内容缺失问题？ • 1.2 如何 解决 内容缺失问题？ • 问题二：错过排名靠前的文档 • 2.1 介绍一下 错过排名靠前的文档 问题？ • 2.2 如何 解决 错过排名靠前的文档 问题？ • 问题三：脱离上下文 — 整合策略的限制 • 3.1 介绍一下 脱离上下文 — 整

## 代表性原文片段

### 片段 1

大模型（LLMs）RAG —— 关键痛点及对应解决方案
来自： AiGC面试宝典
宁静致远 2024年03月19日 22:30
• 大模型（LLMs）RAG —— 关键痛点及对应解决方案
• 前言
• 问题一：内容缺失问题
• 1.1 介绍一下 内容缺失问题？
• 1.2 如何 解决 内容缺失问题？
• 问题二：错过排名靠前的文档
• 2.1 介绍一下 错过排名靠前的文档 问题？
• 2.2 如何 解决 错过排名靠前的文档 问题？
• 问题三：脱离上下文 — 整合策略的限制
• 3.1 介绍一下 脱离上下文 — 整合策略的限制 问题？
• 3.2 如何 解决 脱离上下文 — 整合策略的限制 问题？
• 问题四：未能提取答案
• 4.1 介绍一下 未能提取答案 问题？
• 4.2 如何 解决 未能提取答案 问题？
• 问题五：格式错误
• 5.1 介绍一下 格式错误 问题？
• 5.2 如何 解决 格式错误 问题？
• 问题六： 特异性错误
• 6.1 介绍一下 特异性错误 问题？
• 6.2 如何 解决 特异性错误 问题？
• 问题七： 回答不全面
• 7.1 介绍一下 回答不全面 问题？

### 片段 2

• 问题六： 特异性错误
• 6.1 介绍一下 特异性错误 问题？
• 6.2 如何 解决 特异性错误 问题？
• 问题七： 回答不全面
• 7.1 介绍一下 回答不全面 问题？
• 7.2 如何 解决 回答不全面 问题？
• 问题八： 数据处理能力的挑战
• 8.1 介绍一下 数据处理能力的挑战 问题？
• 8.2 如何 解决 数据处理能力的挑战 问题？
• 问题九： 结构化数据查询的难题
• 9.1 介绍一下 结构化数据查询的难题 问题？
• 9.2 如何 解决 结构化数据查询的难题 问题？
• 问题十： 从复杂PDF文件中提取数据
• 10.1 介绍一下 从复杂PDF文件中提取数据 问题？
• 10.2 如何 解决 从复杂PDF文件中提取数据 问题？
• 问题十一： 备用模型
• 11.1 介绍一下 备用模型 问题？
• 11.2 如何 解决 备用模型 问题？
• 问题十二： 大语言模型（LLM）的安全挑战
• 12.1 介绍一下 大语言模型（LLM）的安全挑战 问题？
• 12.2 如何 解决 大语言模型（LLM）的安全挑战 问题？
• 总结
• 致谢
扫码加
查看更多

-- 1 of 15 --

前言

### 片段 3

大语言模型（LLM）的安全挑战 问题？
• 12.2 如何 解决 大语言模型（LLM）的安全挑战 问题？
• 总结
• 致谢
扫码加
查看更多

-- 1 of 15 --

前言
受到 Barnett 等人的论文《Seven Failure Points When Engineering a Retrieval Augmented
Generation System》的启发，本文将探讨论文中提到的七个痛点，以及在开发检索增强型生成
（RAG）流程中常见的五个额外痛点。更为关键的是，我们将深入讨论这些 RAG 痛点的解决策
略，使我们在日常 RAG 开发中能更好地应对这些挑战。
问题一：内容缺失问题
1.1 介绍一下 内容缺失问题？
当实际答案不在知识库中时，RAG 系统往往给出一个貌似合理却错误的答案，而不是承认无法给
出答案。这导致用户接收到误导性信息，造成错误的引导。
1.2 如何 解决 内容缺失问题？
“输入什么，输出什么。”如果源数据质量差，比如充斥着冲突信息，那么无论你如何构建 RAG 流
程，都不可能从杂乱无章的数据中得到有价值的结果。
2. 改进提示方式

### 片段 4

内容缺失问题？
“输入什么，输出什么。”如果源数据质量差，比如充斥着冲突信息，那么无论你如何构建 RAG 流
程，都不可能从杂乱无章的数据中得到有价值的结果。
2. 改进提示方式
在知识库缺乏信息，系统可能给出错误答案的情况下，改进提示方式可以起到显著帮助。
例如，通过设置提示“如果你无法确定答案，请表明你不知道”
可以鼓励模型认识到自己的局限并更透明地表达不确定性。虽然无法保证百分百准确，但在优化数
据源之后，改进提示方式是我们能做的最好努力之一。
问题二：错过排名靠前的文档
2.1 介绍一下 错过排名靠前的文档 问题？
有时候系统在检索资料时，最关键的文件可能并没有出现在返回结果的最前面。这就导致了正确答
案被忽略，系统因此无法给出精准的回答。
即：“问题的答案其实在某个文档里面，只是它没有获得足够高的排名以致于没能呈现给用户”
2.2 如何 解决 错过排名靠前的文档 问题？
在将检索到的结果发送给大型语言模型（LLM）之前，对结果进行重新排名可以显著提升RAG的性
能。LlamaIndex的一个笔记本展示了两种不同方法的效果对比：
1. 优化数据源
1. 重新排名检索结果

-- 2 of 15 --

### 片段 5

结果进行重新排名可以显著提升RAG的性
能。LlamaIndex的一个笔记本展示了两种不同方法的效果对比：
1. 优化数据源
1. 重新排名检索结果

-- 2 of 15 --

2. 调整数据块大小（chunk_size）和相似度排名（similarity_top_k）超参数
chunk_size和similarity_top_k都是用来调控 RAG（检索增强型生成）模型数据检索过程中效率和
效果的参数。改动这些参数能够影响计算效率与信息检索质量之间的平衡。以 LlamaIndex 为例，
下面是一个示例代码片段。
定义函数 objective_function_semantic_similarity，param_dict包含了参数chunk_size和top_k 以及
它们推荐的值：
• 直接检索前两个节点，不进行重新排名，这可能导致不准确的检索结果。
• 先检索前十个节点，然后使用CohereRerank进行重新排名，最后返回前两个节点，这种方法可
以提高检索的准确性。
param_tuner = ParamTuner(

### 片段 6

结果。
• 先检索前十个节点，然后使用CohereRerank进行重新排名，最后返回前两个节点，这种方法可
以提高检索的准确性。
param_tuner = ParamTuner(
param_fn=objective_function_semantic_similarity,
param_dict=param_dict,
fixed_param_dict=fixed_param_dict,
show_progress=True,
)
results = param_tuner.tune()
# 包含需要调优的参数
param_dict = {"chunk_size": [256, 512, 1024], "top_k": [1, 2, 5]}
# 包含在调整过程的所有运行中保持固定的参数
fixed_param_dict = {
"docs": documents,
"eval_qs": eval_qs,
"ref_response_strs": ref_response_strs,
}
def objective_function_semantic_similarity(params_dict):

### 片段 7

ponse_strs": ref_response_strs,
}
def objective_function_semantic_similarity(params_dict):
chunk_size = params_dict["chunk_size"]
docs = params_dict["docs"]
top_k = params_dict["top_k"]
eval_qs = params_dict["eval_qs"]
ref_response_strs = params_dict["ref_response_strs"]
# 建立索引
index = _build_index(chunk_size, docs)
# 查询引擎
query_engine = index.as_query_engine(similarity_top_k=top_k)
# 获得预测响应
pred_response_objs = get_responses(
eval_qs, query_engine, show_progress=True
)
# 运行评估程序

-- 3 of 15 --

问题三：脱离上下文 — 整合策略的限制

### 片段 8

(
eval_qs, query_engine, show_progress=True
)
# 运行评估程序

-- 3 of 15 --

问题三：脱离上下文 — 整合策略的限制
3.1 介绍一下 脱离上下文 — 整合策略的限制 问题？
论文中提到了这样一个问题：“虽然数据库检索到了含有答案的文档，但这些文档并没有被用来生
成答案。这种情况往往出现在数据库返回大量文档后，需要通过一个整合过程来找出答案”。
3.2 如何 解决 脱离上下文 — 整合策略的限制 问题？
以 LlamaIndex 为例，LlamaIndex 提供了一系列从基础到高级的检索策略，以帮助我们在 RAG 流
程中实现精准检索。欲了解所有检索策略的详细分类，可以查阅 retrievers 模块的指南
如果你使用的是开源嵌入模型，对其进行微调是提高检索准确性的有效方法。LlamaIndex 提供了
一份详尽的指南，指导如何一步步微调开源嵌入模型，并证明了微调可以在各项评估指标上持续改
进性能。

### 片段 9

开源嵌入模型，对其进行微调是提高检索准确性的有效方法。LlamaIndex 提供了
一份详尽的指南，指导如何一步步微调开源嵌入模型，并证明了微调可以在各项评估指标上持续改
进性能。
（https://docs.llamaindex.ai/en/stable/examples/finetuning/embeddings/finetune_embedding.html
）
下面是一个示例代码片段，展示了如何创建微调引擎、执行微调以及获取微调后的模型：
eval_batch_runner = _get_eval_batch_runner_semantic_similarity()
eval_results = eval_batch_runner.evaluate_responses(
eval_qs, responses=pred_response_objs, reference=ref_response_strs
)
# 获取语义相似度度量
mean_score = np.array(
[r.score for r in eval_results["semantic_similarity"]]
).mean()

### 片段 10

度度量
mean_score = np.array(
[r.score for r in eval_results["semantic_similarity"]]
).mean()
return RunResult(score=mean_score, params=params_dict)
1. 优化检索策略
• 从每个索引进行基础检索
• 进行高级检索和搜索
• 自动检索
• 知识图谱检索器
• 组合/分层检索器
• 更多其他选项！
1. 微调嵌入模型
finetune_engine = SentenceTransformersFinetuneEngine(
train_dataset,
model_id="BAAI/bge-small-en",
model_output_path="test_model",
val_dataset=val_dataset,
)
finetune_engine.finetune()
embed_model = finetune_engine.get_finetuned_model()

-- 4 of 15 --

问题四：未能提取答案
4.1 介绍一下 未能提取答案 问题？

### 片段 11

del = finetune_engine.get_finetuned_model()

-- 4 of 15 --

问题四：未能提取答案
4.1 介绍一下 未能提取答案 问题？
当系统需要从提供的上下文中提取正确答案时，尤其是在信息量巨大时，系统往往会遇到困难。关
键信息被遗漏，从而影响了回答的质量。
论文中提到：“这种情况通常是由于上下文中存在太多干扰信息或相互矛盾的信息”。
4.2 如何 解决 未能提取答案 问题？
这一痛点再次凸显了数据质量的重要性。我们必须再次强调，干净整洁的数据至关重要！在质疑
RAG 流程之前，务必先要清理数据。
LongLLMLingua 研究项目/论文中提出了长上下文设置中的提示压缩技术。通过将其集成到
LlamaIndex 中，我们现在可以将 LongLLMLingua 作为节点后处理步骤，在检索步骤之后压缩上
下文，然后再将其输入大语言模型。
以下是一个设置 LongLLMLinguaPostprocessor 的示例代码片段，它利用 longllmlingua 包来执行
提示压缩。更多详细信息，请查阅 LongLLMLingua 的完整文档：

### 片段 12

LLMLinguaPostprocessor 的示例代码片段，它利用 longllmlingua 包来执行
提示压缩。更多详细信息，请查阅 LongLLMLingua 的完整文档：
https://docs.llamaindex.ai/en/stable/examples/node_postprocessor/LongLLMLingua.html#longllml
ingua。
1. 清理数据
1. 提示压缩
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.response_synthesizers import CompactAndRefine
from llama_index.postprocessor import LongLLMLinguaPostprocessor
from llama_index.schema import QueryBundle
node_postprocessor = LongLLMLinguaPostprocessor(
instruction_str="鉴于上下文，请回答最后一个问题",

## 使用建议

- 这些内容来自授权公开 PDF 的文本抽取结果，网页端会基于同一份静态索引做关键词检索。
- 面试复习时建议先用网页 PDF 原文检索定位题目，再回到主 notes 学系统化答案。
- 如果片段出现排版噪声，以原 PDF 语义为准，并优先整理成自己的回答模板。
