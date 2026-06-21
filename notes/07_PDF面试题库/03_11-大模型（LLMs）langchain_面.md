# 11-大模型（LLMs）langchain 面

> 来源 PDF：`200页AI大模型面试高频必刷题（附详解）/11-大模型（LLMs）langchain 面.pdf`  
> 主题：RAG / 文档问答  
> 页数：7  
> 字符数：8898  
> 索引片段数：22

## 摘要

大模型（LLMs）langchain 面 来自： AiGC面试宝典 宁静致远 2023年09月16日 21:19 1. 什么是 LangChain? LangChain是一个强大的框架，旨在帮助开发人员使用语言模型构建端到端的应用程序。它提供了一套工具、组 件和接口，可简化创建由大型语言模型 (LLM) 和聊天模型提供支持的应用程序的过程。LangChain 可以轻松管理 与语言模型的交互，将多个组件链接在一起，并集成额外的资源，例如 API 和数据库。 2. LangChain 包含哪些 核心概念？ 2.1 La

## 代表性原文片段

### 片段 1

大模型（LLMs）langchain 面
来自： AiGC面试宝典
宁静致远 2023年09月16日 21:19
1. 什么是 LangChain?
LangChain是一个强大的框架，旨在帮助开发人员使用语言模型构建端到端的应用程序。它提供了一套工具、组
件和接口，可简化创建由大型语言模型 (LLM) 和聊天模型提供支持的应用程序的过程。LangChain 可以轻松管理
与语言模型的交互，将多个组件链接在一起，并集成额外的资源，例如 API 和数据库。
2. LangChain 包含哪些 核心概念？
2.1 LangChain 中 Components and Chains 是什么？
注：一个 Chain 可能包括一个 Prompt 模板、一个语言模型和一个输出解析器，它们一起工作以
处理用户输入、生成响应并处理输出。
2.2 LangChain 中 Prompt Templates and Values 是什么？
2.3 LangChain 中 Example Selectors 是什么？
2.4 LangChain 中 Output Parsers 是什么？

### 片段 2

and Values 是什么？
2.3 LangChain 中 Example Selectors 是什么？
2.4 LangChain 中 Output Parsers 是什么？
2.5 LangChain 中 Indexes and Retrievers 是什么？
Index ：一种组织文档的方式，使语言模型更容易与它们交互；
Retrievers：用于获取相关文档并将它们与语言模型组合的接口；
注：LangChain 提供了用于处理不同类型的索引和检索器的工具和功能，例如矢量数据库和文本拆分器。
2.6 LangChain 中 Chat Message History 是什么？
• Component ：模块化的构建块，可以组合起来创建强大的应用程序；
• Chain ：组合在一起以完成特定任务的一系列 Components（或其他 Chain）；
• Prompt Template 作用：负责创建 PromptValue，这是最终传递给语言模型的内容
• Prompt Template 特点：有助于将用户输入和其他动态信息转换为适合语言模型的格式。PromptValues 是

### 片段 3

PromptValue，这是最终传递给语言模型的内容
• Prompt Template 特点：有助于将用户输入和其他动态信息转换为适合语言模型的格式。PromptValues 是
具有方法的类，这些方法可以转换为每个模型类型期望的确切输入类型（如文本或聊天消息）。
• 作用：当您想要在 Prompts 中动态包含示例时，Example Selectors 很有用。他们接受用户输入并返回一个
示例列表以在提示中使用，使其更强大和特定于上下文。
• 作用： 负责将语言模型响应构建为更有用的格式
• 实现方法：
• 一种用于提供格式化指令
• 另一种用于将语言模型的响应解析为结构化格式
• 特点：使得在您的应用程序中处理输出数据变得更加容易。
• Chat Message History 作用：负责记住所有以前的聊天交互数据，然后可以将这些交互数据传递回模型、汇
总或以其他方式组合；
• 优点：有助于维护上下文并提高模型对对话的理解
扫码加
查看更多

-- 1 of 7 --

2.7 LangChain 中 Agents and Toolkits 是什么？

### 片段 4

• 优点：有助于维护上下文并提高模型对对话的理解
扫码加
查看更多

-- 1 of 7 --

2.7 LangChain 中 Agents and Toolkits 是什么？
通过理解和利用这些核心概念，您可以利用 LangChain 的强大功能来构建适应性强、高效且能够处理复杂用例
的高级语言模型应用程序。
3. 什么是 LangChain Agent?
4. 如何使用 LangChain ?
要使用 LangChain，开发人员首先要导入必要的组件和工具，例如 LLMs, chat models, agents, chains, 内存功
能。这些组件组合起来创建一个可以理解、处理和响应用户输入的应用程序。
5. LangChain 支持哪些功能?
6. 什么是 LangChain model?
LangChain model 是一种抽象，表示框架中使用的不同类型的模型。LangChain 中的模型主要分为三类：
开发人员可以为他们的用例选择合适的 LangChain 模型，并利用提供的组件来构建他们的应用程序。
7. LangChain 包含哪些特点?
LangChain 旨在为六个主要领域的开发人员提供支持：

### 片段 5

例选择合适的 LangChain 模型，并利用提供的组件来构建他们的应用程序。
7. LangChain 包含哪些特点?
LangChain 旨在为六个主要领域的开发人员提供支持：
• Agent ：在 LangChain 中推动决策制定的实体。他们可以访问一套工具，并可以根据用户输入决定调用哪个
工具；
• Tookits ：一组工具，当它们一起使用时，可以完成特定的任务。代理执行器负责使用适当的工具运行代理。
• 介绍：LangChain Agent 是框架中驱动决策制定的实体。它可以访问一组工具，并可以根据用户的输入决定
调用哪个工具；
• 优点：LangChain Agent 帮助构建复杂的应用程序，这些应用程序需要自适应和特定于上下文的响应。当存
在取决于用户输入和其他因素的未知交互链时，它们特别有用。
• 针对特定文档的问答：根据给定的文档回答问题，使用这些文档中的信息来创建答案。
• 聊天机器人：构建可以利用 LLM 的功能生成文本的聊天机器人。
• Agents：开发可以决定行动、采取这些行动、观察结果并继续执行直到完成的代理。

### 片段 6

些文档中的信息来创建答案。
• 聊天机器人：构建可以利用 LLM 的功能生成文本的聊天机器人。
• Agents：开发可以决定行动、采取这些行动、观察结果并继续执行直到完成的代理。
1. LLM（大型语言模型）：这些模型将文本字符串作为输入并返回文本字符串作为输出。它们是许多语言模型
应用程序的支柱。
2. 聊天模型( Chat Model)：聊天模型由语言模型支持，但具有更结构化的 API。他们将聊天消息列表作为输入
并返回聊天消息。这使得管理对话历史记录和维护上下文变得容易。
3. 文本嵌入模型(Text Embedding Models)：这些模型将文本作为输入并返回表示文本嵌入的浮点列表。这些
嵌入可用于文档检索、聚类和相似性比较等任务。
1. LLM 和提示：LangChain 使管理提示、优化它们以及为所有 LLM 创建通用界面变得容易。此外，它还包括
一些用于处理 LLM 的便捷实用程序。
2. 链(Chain)：这些是对 LLM 或其他实用程序的调用序列。LangChain 为链提供标准接口，与各种工具集成，
为流行应用提供端到端的链。

### 片段 7

理 LLM 的便捷实用程序。
2. 链(Chain)：这些是对 LLM 或其他实用程序的调用序列。LangChain 为链提供标准接口，与各种工具集成，
为流行应用提供端到端的链。
3. 数据增强生成：LangChain 使链能够与外部数据源交互以收集生成步骤的数据。例如，它可以帮助总结长文
本或使用特定数据源回答问题。
4. Agents：Agents 让 LLM 做出有关行动的决定，采取这些行动，检查结果，并继续前进直到工作完成。
LangChain 提供了代理的标准接口，多种代理可供选择，以及端到端的代理示例。
5. 内存：LangChain 有一个标准的内存接口，有助于维护链或代理调用之间的状态。它还提供了一系列内存实
现和使用内存的链或代理的示例。
6. 评估：很难用传统指标评估生成模型。这就是为什么 LangChain 提供提示和链来帮助开发者自己使用 LLM
评估他们的模型。

-- 2 of 7 --

8. LangChain 如何使用?
8.1 LangChain 如何调用 LLMs 生成回复？
Models: 指各类训练好大语言模型（eg: chatgpt(未开源)，chatglm，vicuna等）

### 片段 8

如何使用?
8.1 LangChain 如何调用 LLMs 生成回复？
Models: 指各类训练好大语言模型（eg: chatgpt(未开源)，chatglm，vicuna等）
8.2 LangChain 如何修改 提示模板？
langchain.PromptTemplate: langchain中的提示模板类
根据不同的下游任务设计不同的prompt模板，然后填入内容，生成新的prompt。目的其实就是为了通过设计更准
确的提示词，来引导大模型输出更合理的内容。
# 官方llm使用OPENAI 接口
from langchain.llms import OpenAI
llm = OpenAI(model_name="text-davinci-003")
prompt = "你好"
response = llm(prompt)
# 你好，我是chatGPT,很高兴能够和你聊天。有什么我可以帮助你的吗？
-我们用chatglm来演示该过程，封装一下即可
from transformers import AutoTokenizer, AutoModel
class chatGLM():

### 片段 9

我们用chatglm来演示该过程，封装一下即可
from transformers import AutoTokenizer, AutoModel
class chatGLM():
def __init__(self, model_name) -> None:
self.tokenizer = AutoTokenizer.from_pretrained(model_name,
trust_remote_code=True)
self.model = AutoModel.from_pretrained(model_name,
trust_remote_code=True).half().cuda().eval()
def __call__(self, prompt) -> Any:
response, _ = self.model.chat(self.tokenizer , prompt) # 这里演示未使用流式
接口. stream_chat()
return response
llm = chatGLM(model_name="THUDM/chatglm-6b")
prompt = "你好"

### 片段 10

. stream_chat()
return response
llm = chatGLM(model_name="THUDM/chatglm-6b")
prompt = "你好"
response = llm(prompt)
print("response: %s"%response)
“”“
response: 你好 ！我是人工智能助手 ChatGLM-6B，很高兴见到你，欢迎问我任何问题。
”“”
from langchain import PromptTemplate
template = """
Explain the concept of {concept} in couple of lines
"""
prompt = PromptTemplate(input_variables=["concept"], template=template)
prompt = prompt.format(concept="regularization")
print(“prompt=%s”%prompt)

### 片段 11

plate=template)
prompt = prompt.format(concept="regularization")
print(“prompt=%s”%prompt)
#'\nExplain the concept of regularization in couple of lines\n'

-- 3 of 7 --

8.3 LangChain 如何链接多个组件处理一个特定的下游任务？
8.4 LangChain 如何Embedding & vector store？
Emebdding这个过程想必大家很熟悉，简单理解就是把现实中的信息通过各类算法编码成一个高维向量，便于计
算机快速计算。
-------------------------
template = "请给我解释一下{concept}的意思"
prompt = PromptTemplate(input_variables=["concept"], template=template)
prompt = prompt.format(concept="人工智能")
print(“prompt=%s”%prompt)

### 片段 12

ept"], template=template)
prompt = prompt.format(concept="人工智能")
print(“prompt=%s”%prompt)
#'\n请给我解释一下人工智能的意思\n'
#chains ---------
from langchain.chains import LLMChain
chain = LLMChain(llm=openAI(), prompt=promptTem)
print(chain.run("你好"))
#chains ---------Chatglm对象不符合LLMChain类llm对象要求，模仿一下
class DemoChain():
def __init__(self, llm, prompt) -> None:
self.llm = llm
self.prompt = prompt
def run(self, query) -> Any:
prompt = self.prompt.format(concept=query)
print("query=%s ->prompt=%s"%(query, prompt))

## 使用建议

- 这些内容来自授权公开 PDF 的文本抽取结果，网页端会基于同一份静态索引做关键词检索。
- 面试复习时建议先用网页 PDF 原文检索定位题目，再回到主 notes 学系统化答案。
- 如果片段出现排版噪声，以原 PDF 语义为准，并优先整理成自己的回答模板。
