# 21-RAG（Retrieval-Augmented Generation）评测面

> 来源 PDF：`200页AI大模型面试高频必刷题（附详解）/21-RAG（Retrieval-Augmented Generation）评测面.pdf`  
> 主题：RAG / 文档问答  
> 页数：10  
> 字符数：10521  
> 索引片段数：26

## 摘要

RAG（Retrieval-Augmented Generation）评测面 来自： AiGC面试宝典 宁静致远 2024年01月28日 10:12 一、为什么需要 对 RAG 进行评测？ 在探索和优化 RAG（检索增强生成器）的过程中，如何有效评估其性能已经成为关键问题。 二、如何合成 RAG 测试集？ 假设你已经成功构建了一个RAG 系统，并且现在想要评估它的性能。为了这个目的，你需要一个 评估数据集，该数据集包含以下列： 前两列代表真实数据，最后两列代表 RAG 预测数据。 要创建这样的数据集，我们首先需要生

## 代表性原文片段

### 片段 1

RAG（Retrieval-Augmented Generation）评测面
来自： AiGC面试宝典
宁静致远 2024年01月28日 10:12
一、为什么需要 对 RAG 进行评测？
在探索和优化 RAG（检索增强生成器）的过程中，如何有效评估其性能已经成为关键问题。
二、如何合成 RAG 测试集？
假设你已经成功构建了一个RAG 系统，并且现在想要评估它的性能。为了这个目的，你需要一个
评估数据集，该数据集包含以下列：
前两列代表真实数据，最后两列代表 RAG 预测数据。
要创建这样的数据集，我们首先需要生成问题和答案的元组。
接下来，在RAG上运行这些问题以获得预测结果。
要生成（问题、答案）元组，我们首先需要准备 RAG 数据，我们将其拆分为块，并将其嵌入向量
数据库中。 完成这些步骤后，我们会指示 LLM 从指定主题中生成 num_questions 个问题，从而得
• RAG（Retrieval-Augmented Generation）评测面
• 一、为什么需要 对 RAG 进行评测？
• 二、如何合成 RAG 测试集？
• 三、RAG 有哪些评估方法？
• 3.1 独立评估

### 片段 2

gmented Generation）评测面
• 一、为什么需要 对 RAG 进行评测？
• 二、如何合成 RAG 测试集？
• 三、RAG 有哪些评估方法？
• 3.1 独立评估
• 3.1.1 介绍一下 独立评估？
• 3.1.2 介绍一下 独立评估 模块？
• 3.2 端到端评估
• 3.2.1 介绍一下 端到端评估
• 3.2.2 介绍一下 端到端评估 模块？
• 四、RAG 有哪些关键指标和能力？
• 五、RAG 有哪些评估框架？
• 4.1 RAGAS
• 4.2 ARES
• 致谢
• question（问题）：想要评估的RAG的问题
• ground_truths（真实答案）：问题的真实答案
• answer（答案）：RAG 预测的答案
• contexts（上下文）：RAG 用于生成答案的相关信息列表
• 生成问题和基准答案（实践中可能会出现偏差）
扫码加
查看更多

-- 1 of 10 --

到问题和答案元组。
为了从给定的上下文中生成问题和答案，我们需要按照以下步骤操作：
1. 选择一个随机块并将其作为根上下文
2. 从向量数据库中检索 K 个相似的上下文

### 片段 3

0 --

到问题和答案元组。
为了从给定的上下文中生成问题和答案，我们需要按照以下步骤操作：
1. 选择一个随机块并将其作为根上下文
2. 从向量数据库中检索 K 个相似的上下文
3. 将根上下文和其 K 个相邻上下文的文本连接起来以构建一个更大的上下文
4. 使用这个大的上下文和 num_questions 在以下的提示模板中生成问题和答案
"""\\
Your task is to formulate exactly {num_questions} questions from given context and
provide the answer to each one.
End each question with a '?' character and then in a newline write the answer to
that question using only
the context provided.
Separate each question/answer pair by "XXX"
Each question must start with "question:".

### 片段 4

ed.
Separate each question/answer pair by "XXX"
Each question must start with "question:".
Each answer must start with "answer:".
The question must satisfy the rules given below:
1.The question should make sense to humans even when read without the given
context.
2.The question should be fully answered from the given context.
3.The question should be framed from a part of context that contains important
information. It can also be from tables,code,etc.
4.The answer to the question should not contain any links.

### 片段 5

n also be from tables,code,etc.
4.The answer to the question should not contain any links.
5.The question should be of moderate difficulty.
6.The question must be reasonable and must be understood and responded by humans.
7.Do no use phrases like 'provided context',etc in the question
8.Avoid framing question using word "and" that can be decomposed into more than one
question.
9.The question should not contain more than 10 words, make of use of abbreviation
wherever possible.
context: {context}
"""
"""\\

### 片段 6

than 10 words, make of use of abbreviation
wherever possible.
context: {context}
"""
"""\\
您的任务是根据给定的上下文提出{num_questions}个问题，并给出每个问题的答案。
在每个问题的末尾加上"?
提供的上下文写出该问题的答案。
每个问题/答案之间用 "XXX "隔开。
每个问题必须以 "question: "开头。
每个答案必须以 "answer: "开头。
问题必须符合以下规则：
1.即使在没有给定上下文的情况下，问题也应该对人类有意义。

-- 2 of 10 --

基于上面的工作流程，下面是我生成问题和答案的结果示例。
首先构建一个向量存储，其中包含 RAG 使用的数据。
2.问题应能根据给定的上下文给出完整的答案。
3.问题应从包含重要信息的上下文中提取。也可以是表格、代码等。
4.问题答案不应包含任何链接。
5.问题难度应适中。
6.问题必须合理，必须为人类所理解和回答。
7.不要在问题中使用 "提供上下文 "等短语。
8.避免在问题中使用 "和 "字，因为它可以分解成多个问题。

### 片段 7

接。
5.问题难度应适中。
6.问题必须合理，必须为人类所理解和回答。
7.不要在问题中使用 "提供上下文 "等短语。
8.避免在问题中使用 "和 "字，因为它可以分解成多个问题。
9.问题不应超过 10 个单词，尽可能使用缩写。
语境： {上下文｝
"""
5. 重复以上步骤 num_count 次,每次改变上下文并生成不同的问题。
| | question | ground_truths
|
|---:|:---------------------------------------------------|:-----------------------
----------------------------|
| 8 | What is the difference between lists and tuples in | ['Lists are mutable and
cannot be used as |
| | Python? | dictionary keys, while
tuples are immutable and |
| | | can be used as

### 片段 8

as |
| | Python? | dictionary keys, while
tuples are immutable and |
| | | can be used as
dictionary keys if all elements are |
| | | immutable.']
|
| 4 | What is the name of the Python variant optimized | ['MicroPython and
CircuitPython'] |
| | for microcontrollers? |
|
| 13 | What is the name of the programming language that | ['ABC programming
language'] |
| | Python was designed to replace? |
|
| 17 | How often do bugfix releases occur? | ['Bugfix releases occur
about every 3 months.'] |

### 片段 9

| How often do bugfix releases occur? | ['Bugfix releases occur
about every 3 months.'] |
| 3 | What is the significance of Python's release | ['Python 2.0 was
released in 2000, while Python |
| | history? | 3.0, a major revision
with limited backward |
| | | compatibility, was
released in 2008.'] |
• 编码用例
1. 我们从 Wikipedia 加载它
from langchain.document_loaders import WikipediaLoader

-- 3 of 10 --

topic = "python programming"
wikipedia_loader = WikipediaLoader(
query=topic,
load_max_docs=1,

### 片段 10

c = "python programming"
wikipedia_loader = WikipediaLoader(
query=topic,
load_max_docs=1,
doc_content_chars_max=100000,
)
docs = wikipedia_loader.load()
doc = docs[0]
2. 加载数据后，我们将其分成块。
from langchain.text_splitter import RecursiveCharacterTextSplitter
CHUNK_SIZE = 512
CHUNK_OVERLAP = 128
splitter = RecursiveCharacterTextSplitter(
chunk_size=CHUNK_SIZE,
chunk_overlap=CHUNK_OVERLAP,
separators=[". "],
)
splits = splitter.split_documents([doc])
3. 在 Pinecone 中创建一个索引。
import pinecone
pinecone.init(

### 片段 11

ts = splitter.split_documents([doc])
3. 在 Pinecone 中创建一个索引。
import pinecone
pinecone.init(
api_key=os.environ.get("PINECONE_API_KEY"),
environment=os.environ.get("PINECONE_ENV"),
)
index_name = topic.replace(" ", "-")
pinecone.init(
api_key=os.environ.get("PINECONE_API_KEY"),
environment=os.environ.get("PINECONE_ENV"),
)
if index_name in pinecone.list_indexes():
pinecone.delete_index(index_name)
pinecone.create_index(index_name, dimension=768)
4. 使用 LangChain 包装器来索引其中的分片嵌入。

### 片段 12

ndex_name)
pinecone.create_index(index_name, dimension=768)
4. 使用 LangChain 包装器来索引其中的分片嵌入。
from langchain.vectorstores import Pinecone
docsearch = Pinecone.from_documents(
splits,
embedding_model,
index_name=index_name,
)
5. 生成合成数据集

-- 4 of 10 --

我们使用 LLM、文档拆分、嵌入模型和 Pinecone 索引名称从TestsetGenerator 类初始化一个对
象。
from langchain.embeddings import VertexAIEmbeddings
from langchain.llms import VertexAI
from testset_generator import TestsetGenerator
generator_llm = VertexAI(
location="europe-west3",
max_output_tokens=256,

## 使用建议

- 这些内容来自授权公开 PDF 的文本抽取结果，网页端会基于同一份静态索引做关键词检索。
- 面试复习时建议先用网页 PDF 原文检索定位题目，再回到主 notes 学系统化答案。
- 如果片段出现排版噪声，以原 PDF 语义为准，并优先整理成自己的回答模板。
