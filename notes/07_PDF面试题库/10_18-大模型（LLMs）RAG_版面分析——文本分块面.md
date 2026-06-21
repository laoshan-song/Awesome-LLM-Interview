# 18-大模型（LLMs）RAG 版面分析——文本分块面

> 来源 PDF：`200页AI大模型面试高频必刷题（附详解）/18-大模型（LLMs）RAG 版面分析——文本分块面.pdf`  
> 主题：RAG / 文档问答  
> 页数：8  
> 字符数：8789  
> 索引片段数：22

## 摘要

大模型（LLMs）RAG 版面分析——文本分块面 来自： AiGC面试宝典 宁静致远 2024年03月19日 22:30 一、为什么需要对文本分块？ 使用大型语言模型（LLM）时，切勿忽略文本分块的重要性，其对处理结果的好坏有重大影响。 考虑以下场景：你面临一个几百页的文档，其中充满了文字，你希望对其进行摘录和问答式处 理。在这个流程中，最初的一步是提取文档的嵌入向量，但这样做会带来几个问题： 因此，恰当地实施文本分块不仅能够提升文本的整体品质和可读性，还能够预防由于信息丢失或不 当分块引起的问题。这就是为何在处理

## 代表性原文片段

### 片段 1

大模型（LLMs）RAG 版面分析——文本分块面
来自： AiGC面试宝典
宁静致远 2024年03月19日 22:30
一、为什么需要对文本分块？
使用大型语言模型（LLM）时，切勿忽略文本分块的重要性，其对处理结果的好坏有重大影响。
考虑以下场景：你面临一个几百页的文档，其中充满了文字，你希望对其进行摘录和问答式处
理。在这个流程中，最初的一步是提取文档的嵌入向量，但这样做会带来几个问题：
因此，恰当地实施文本分块不仅能够提升文本的整体品质和可读性，还能够预防由于信息丢失或不
当分块引起的问题。这就是为何在处理长篇文档时，采用文本分块而非直接处理整个文档至关重要
的原因。
二、能不能介绍一下常见的文本分块方法？
2.1 一般的文本分块方法
如果不借助任何包，直接按限制长度切分方案：
• 大模型（LLMs）RAG 版面分析——文本分块面
• 一、为什么需要对文本分块？
• 二、能不能介绍一下常见的文本分块方法？
• 2.1 一般的文本分块方法
• 2.2 正则拆分的文本分块方法
• 2.3 Spacy Text Splitter 方法

### 片段 2

文本分块？
• 二、能不能介绍一下常见的文本分块方法？
• 2.1 一般的文本分块方法
• 2.2 正则拆分的文本分块方法
• 2.3 Spacy Text Splitter 方法
• 2.4 基于 langchain 的 CharacterTextSplitter 方法
• 2.5 基于 langchain 的 递归字符切分 方法
• 2.6 HTML 文本拆分 方法
• 2.7 Mrrkdown 文本拆分 方法
• 2.8 Python代码拆分 方法
• 2.9 LaTex 文本拆分 方法
• 致谢
• 信息丢失的风险：试图一次性提取整个文档的嵌入向量，虽然可以捕捉到整体的上下文，但也
可能会忽略掉许多针对特定主题的重要信息，这可能会导致生成的信息不够精确或者有所缺
失。
• 分块大小的限制：在使用如OpenAI这样的模型时，分块大小是一个关键的限制因素。例如，
GPT-4模型有一个32K的窗口大小限制。尽管这个限制在大多数情况下不是问题，但从一开始
就考虑到分块大小是很重要的。
text = "我是一个名为 ChatGLM3-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI

### 片段 3

制在大多数情况下不是问题，但从一开始
就考虑到分块大小是很重要的。
text = "我是一个名为 ChatGLM3-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI
公司于 2023 年共同训练的语言模型开发的。我的目标是通过回答用户提出的问题来帮助他们
解决问题。由于我是一个计算机程序，所以我没有实际的存在，只能通过互联网来与用户交
流。"
chunks = []
扫码加
查看更多

-- 1 of 8 --

2.2 正则拆分的文本分块方法
chunk_size = 128
for i in range(0, len(text), chunk_size):
chunk = text[i:i + chunk_size]
chunks.append(chunk)
chunks
>>>
[
'我是一个名为 ChatGLM3-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI 公
司于 2023 年共同训练的语言模型开发的。我的目标是通过回答用户提出的问题来帮助他们解
决问题。由于我是一个计算机程序，所以我没有实际的存在，只能通过互联网',
'来与用户交流。'
]

### 片段 4

2023 年共同训练的语言模型开发的。我的目标是通过回答用户提出的问题来帮助他们解
决问题。由于我是一个计算机程序，所以我没有实际的存在，只能通过互联网',
'来与用户交流。'
]
• 动机：【一般的文本分块方法】能够按长度进行分割，但是对于一些长度偏长的句子，容易从
中间切开；
• 方法：在中文文本分块的场景中，正则表达式可以用来识别中文标点符号，从而将文本拆分成
单独的句子。这种方法依赖于中文句号、“问号”、“感叹号”等标点符号作为句子结束的标志。
• 特点：虽然这种基于模式匹配的方法可能不如基于复杂语法和语义分析的方法精确，但它在大
多数情况下足以满足基本的句子分割需求，并且实现起来更为简单直接。
import re
def split_sentences(text):
# 使用正则表达式匹配中文句子结束的标点符号
sentence_delimiters = re.compile(u'[。？！；]|\n')
sentences = sentence_delimiters.split(text)
# 过滤掉空字符串

### 片段 5

elimiters = re.compile(u'[。？！；]|\n')
sentences = sentence_delimiters.split(text)
# 过滤掉空字符串
sentences = [s.strip() for s in sentences if s.strip()]
return sentences
text ="文本分块是自然语言处理（NLP）中的一项关键技术，其作用是将较长的文本切割成更
小、更易于处理的片段。这种分割通常是基于单词的词性和语法结构，例如将文本拆分为名词
短语、动词短语或其他语义单位。这样做有助于更高效地从文本中提取关键信息。"
sentences = split_sentences(text)
print(sentences)
>>>
#output
[
'文本分块是自然语言处理（NLP）中的一项关键技术，其作用是将较长的文本切割成更
小、更易于处理的片段',
'这种分割通常是基于单词的词性和语法结构，例如将文本拆分为名词短语、动词短语或其
他语义单位',
'这样做有助于更高效地从文本中提取关键信息'
]

-- 2 of 8 --

### 片段 6

,
'这种分割通常是基于单词的词性和语法结构，例如将文本拆分为名词短语、动词短语或其
他语义单位',
'这样做有助于更高效地从文本中提取关键信息'
]

-- 2 of 8 --

在上面例子中，我们并没有采用任何特定的方式来分割句子。另外，还有许多其他的文本分块技术
可以使用，例如词汇化（tokenizing）、词性标注（POS tagging）等。
2.3 Spacy Text Splitter 方法
2.4 基于 langchain 的 CharacterTextSplitter 方法
使用CharacterTextSplitter，一般的设置参数为：chunk_size、 chunk_overlap、separator和
strip_whitespace。
• 介绍：Spacy是一个用于执行自然语言处理（NLP）各种任务的库。它具有文本拆分器功能，
能够在进行文本分割的同时，保留分割结果的上下文信息。
import spacy
input_text = "文本分块是自然语言处理（NLP）中的一项关键技术，其作用是将较长的文本切
割成更小、更易于处理的片段。这种分割通常是基于单词的词性和语法结构，例如将文本拆分

### 片段 7

put_text = "文本分块是自然语言处理（NLP）中的一项关键技术，其作用是将较长的文本切
割成更小、更易于处理的片段。这种分割通常是基于单词的词性和语法结构，例如将文本拆分
为名词短语、动词短语或其他语义单位。这样做有助于更高效地从文本中提取关键信息。"
nlp = spacy.load( "zh_core_web_sm" )
doc = nlp(input_text)
for s in doc.sents:
print (s)
>>>
[
'文本分块是自然语言处理（NLP）中的一项关键技术，其作用是将较长的文本切割成更
小、更易于处理的片段。',
"这种分割通常是基于单词的词性和语法结构，例如将文本拆分为名词短语、动词短语或其
他语义单位。",
"这样做有助于更高效地从文本中提取关键信息。"
]
from langchain.text_splitter import CharacterTextSplitter
text_splitter = CharacterTextSplitter(chunk_size = 35, chunk_overlap=0,

### 片段 8

racterTextSplitter
text_splitter = CharacterTextSplitter(chunk_size = 35, chunk_overlap=0,
separator='', strip_whitespace=False)
text_splitter.create_documents([text])
>>>
[
Document(page_content='我是一个名为 ChatGLM3-6B 的人工智能助手，是基于清华大学
'),
Document(page_content='KEG 实验室和智谱 AI 公司于 2023 年共同训练的语言模型开
发'),
Document(page_content='的。我的目标是通过回答用户提出的问题来帮助他们解决问题。
由于我是一个计'),
Document(page_content='算机程序，所以我没有实际的存在，只能通过互联网来与用户交
流。')
]

-- 3 of 8 --

2.5 基于 langchain 的 递归字符切分 方法

### 片段 9

e_content='算机程序，所以我没有实际的存在，只能通过互联网来与用户交
流。')
]

-- 3 of 8 --

2.5 基于 langchain 的 递归字符切分 方法
使用RecursiveCharacterTextSplitter，一般的设置参数为：chunk_size、 chunk_overlap。
与CharacterTextSplitter不同，RecursiveCharacterTextSplitter不需要设置分隔符，默认的几个分隔
符如下：
拆分器首先查找两个换行符（段落分隔符）。一旦段落被分割，它就会查看块的大小，如果块太
大，那么它会被下一个分隔符分割。如果块仍然太大，那么它将移动到下一个块上，以此类推。
2.6 HTML 文本拆分 方法
#input text
input_text = "文本分块是自然语言处理（NLP）中的一项关键技术，其作用是将较长的文本切
割成更小、更易于处理的片段。这种分割通常是基于单词的词性和语法结构，例如将文本拆分
为名词短语、动词短语或其他语义单位。这样做有助于更高效地从文本中提取关键信息。"

### 片段 10

将较长的文本切
割成更小、更易于处理的片段。这种分割通常是基于单词的词性和语法结构，例如将文本拆分
为名词短语、动词短语或其他语义单位。这样做有助于更高效地从文本中提取关键信息。"
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
chunk_size = 100 , #设置所需的文本大小
chunk_overlap = 20 )
chunks = text_splitter.create_documents([input_text])
print (chunks)
>>>
[
Document(page_content='文本分块是自然语言处理（NLP）中的一项关键技术，其作用是
将较长的文本切割成更小、更易于处理的片段。这种分割通常是基于单词的词性和语法结构，
例如将文本拆分为名词短语、动词短语或其他语义单位。这样做有助'),
Document(page_content='短语、动词短语或其他语义单位。这样做有助于更高效地从文本

### 片段 11

法结构，
例如将文本拆分为名词短语、动词短语或其他语义单位。这样做有助'),
Document(page_content='短语、动词短语或其他语义单位。这样做有助于更高效地从文本
中提取关键信息。')]
"\n\n" - 两个换行符，一般认为是段落分隔符
"\n" - 换行符
" " - 空格
"" - 字符
• 介绍：HTML文本拆分器是一种结构感知的文本分块工具。它能够在HTML元素级别上进行文本
拆分，并且会为每个分块添加与之相关的标题元数据。
• 特点：对HTML结构的敏感性，能够精准地处理和分析HTML文档中的内容。
#input html string
html_string = """
<!DOCTYPE html>
<html>
<body>
<div>
<h1>Mobot</h1>
<p>一些关于Mobot的介绍文字。</p>

-- 4 of 8 --

仅提取在header_to_split_on参数中指定的HTML标题。
<div>
<h2>Mobot主要部分</h2>
<p>有关Mobot的一些介绍文本。</p>
<h3>Mobot第1小节</h3>

### 片段 12

o_split_on参数中指定的HTML标题。
<div>
<h2>Mobot主要部分</h2>
<p>有关Mobot的一些介绍文本。</p>
<h3>Mobot第1小节</h3>
<p>有关Mobot第一个子主题的一些文本。</p>
<h3>Mobot第2小节</h3>
<p>关于Mobot的第二个子主题的一些文字。</p>
</div>
<div>
<h2>Mobot</h2>
<p>关于Mobot的一些文字</p>
</ div>
<br>
<p>关于Mobot的一些结论性文字</p>
</div>
</body>
</html>
"""
headers_to_split_on = [
( "h1" , "Header 1" ),
( "h2" , "标题 2" ),
( "h3" , "标题 3" ),
]
from langchain.text_splitter import HTMLHeaderTextSplitter
html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

## 使用建议

- 这些内容来自授权公开 PDF 的文本抽取结果，网页端会基于同一份静态索引做关键词检索。
- 面试复习时建议先用网页 PDF 原文检索定位题目，再回到主 notes 学系统化答案。
- 如果片段出现排版噪声，以原 PDF 语义为准，并优先整理成自己的回答模板。
