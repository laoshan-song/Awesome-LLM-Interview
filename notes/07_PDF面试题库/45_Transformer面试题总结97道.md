# Transformer面试题总结97道

> 来源 PDF：`Transformer面试题总结97道.pdf`  
> 主题：RAG / 文档问答  
> 页数：72  
> 字符数：62184  
> 索引片段数：153

## 摘要

Transformer 面试题总结 97 道 1，请阐述 Transformer 能够进行训练来表达和生成信息背后的数学假设，什么数学模型 在 Transformer 模型中，一个关键的数学模型是自注意力机制（Self-Attention Mechanism）。自 注意力机制允许模型在处理序列数据时，同时考虑序列中不同位置之间的依赖关系，从而更好地捕捉 上下文信息。 假设我们有一个输入序列 ,其中 是第 i 个位置的词嵌入向量，我们的目标是通 过 Transformer 模型来预测下一个词 。Transformer

## 代表性原文片段

### 片段 1

Transformer 面试题总结 97 道
1，请阐述 Transformer 能够进行训练来表达和生成信息背后的数学假设，什么数学模型
在 Transformer 模型中，一个关键的数学模型是自注意力机制（Self-Attention Mechanism）。自
注意力机制允许模型在处理序列数据时，同时考虑序列中不同位置之间的依赖关系，从而更好地捕捉
上下文信息。
假设我们有一个输入序列 ,其中 是第 i 个位置的词嵌入向量，我们的目标是通
过 Transformer 模型来预测下一个词 。Transformer 模型的训练目标是最大化下一个词的条件概率：
其中 是一个表示预测 的得分函数。
在 Transformer 模型中，通过注意力权重的加权求和来计算预测得分。具体地，得分函数可以表示
为：
其中 是注意力权重，表示模型在预测时对第 i 个位置的关注程度， 是一个表示预测
和第 i 个位置的词的关联程度的函数。
为 了 计 算 注 意 力 权 重 ， Transformer 模 型 使 用 了 Scaled Dot-Product Attention 机 制 ：

### 片段 2

位置的词的关联程度的函数。
为 了 计 算 注 意 力 权 重 ， Transformer 模 型 使 用 了 Scaled Dot-Product Attention 机 制 ：
其中 和 分别是查询向量和键向量，由输入序列的词嵌入向量经过线性变换得到，
是查询向量和键向量的维度。
2，Transformer 中的可训练 Queries、Keys 和 Values 矩阵从哪儿来？Transformer 中为何
会有 Queries、Keys 和 Values 矩阵，只设置 Values 矩阵本身来求 Attention 不是更简单吗？
Queries（查询）、Keys（键）和 Values（值）矩阵是通过线性变换从输入的词嵌入向量得到的。
这些矩阵是通过训练得到的，它们的作用是将输入的词嵌入向量映射到更高维度的空间，并且通过学
习过程中逐渐调整其中的参数，以使模型能够更好地捕捉输入序列中的语义信息和关系。
这是因为在自注意力机制（Self-Attention Mechanism）中，需要通过 Queries 和 Keys 的相互关

-- 1 of 72 --

### 片段 3

中的语义信息和关系。
这是因为在自注意力机制（Self-Attention Mechanism）中，需要通过 Queries 和 Keys 的相互关

-- 1 of 72 --

联度来计算注意力权重，然后再根据这些权重对 Values 进行加权求和。这种设计的优势在于能够允
许模型在计算注意力时同时考虑到不同位置之间的依赖关系，从而更好地捕捉到输入序列中的上下文
信息。
至于为什么不只设置 Values 矩阵来求 Attention，而是要同时使用 Queries 和 Keys 矩阵，原因在
于 Queries 和 Keys 矩阵能够提供更丰富的信息，从而使模型能够更准确地计算注意力权重。只使用
Values 矩阵可能会限制模型的表达能力，无法充分利用输入序列中的信息。
3，Transformer 的 Feed Forward 层在训练的时候到底在训练什么？
Feed Forward 层在 Transformer 中的训练过程中，通过特征提取和非线性映射来学习输入序列的表
示，从而为模型的下游任务提供更好的输入特征。在训练过程中，Feed Forward 层的参数是通过反

### 片段 4

ansformer 中的训练过程中，通过特征提取和非线性映射来学习输入序列的表
示，从而为模型的下游任务提供更好的输入特征。在训练过程中，Feed Forward 层的参数是通过反
向传播算法和梯度下降优化方法来学习的。通过最小化模型在训练集上的损失函数，模型会自动调整
Feed Forward 层中的权重和偏置，以使得模型能够更好地拟合训练数据，并且在未见过的数据上具
有良好的泛化能力。
4，请具体分析 Transformer 的 Embeddigns 层、Attention 层和 Feedforward 层的复杂度
Transformer 中的 Embedding 层、Attention 层和 Feedforward 层的复杂度：
Embedding 层：
Attention 层：
多头：
Feedforward 层：
其中，n 是序列长度， 是词嵌入维度， 是注意力头中的维度，h 是注意力头的数量， 是
隐藏层的大小。
5，Transformer 的 Positional Encoding 是如何表达相对位置关系的，位置信息在不同的
Encoder 的之间传递会丢失吗？

### 片段 5

数量， 是
隐藏层的大小。
5，Transformer 的 Positional Encoding 是如何表达相对位置关系的，位置信息在不同的
Encoder 的之间传递会丢失吗？
Transformer 中的 Positional Encoding 用于向输入的词嵌入中添加位置信息，以便模型能够理解输

-- 2 of 72 --

入序列中词语的位置顺序。Positional Encoding 通常是通过将位置信息编码成一个固定长度的向量，
并将其与词嵌入相加来实现的。
Positional Encoding 的一种常见表达方式是使用正弦和余弦函数，通过计算不同位置的位置编码向
量来表示相对位置关系。具体来说，位置 pos 的位置编码 PE(pos)可以表示为：
其中，pos 是位置，i 是位置编码向量中的维度索引， 是词嵌入维度。这种位置编码方式允许
模型学习到不同位置之间的相对位置关系，同时能够保持一定的周期性。
至于位置信息在不同的 Encoder 之间是否会丢失，答案是不会。在 Transformer 模型中，位置编码

### 片段 6

许
模型学习到不同位置之间的相对位置关系，同时能够保持一定的周期性。
至于位置信息在不同的 Encoder 之间是否会丢失，答案是不会。在 Transformer 模型中，位置编码
是在每个 Encoder 和 Decoder 层中加入的，并且会随着词嵌入一起流经整个模型。因此，每个
Encoder 和 Decoder 层都会接收到包含位置信息的输入向量，从而能够保留输入序列的位置关系。
这样，位置信息可以在不同的 Encoder 之间传递，并且不会丢失。
AI 大模型入门路线，视频教程，PDF+课件资料包已全部备好，需要的扫码添加，
我会发给你的~
6，Transformer 中的 Layer Normalization 蕴含的神经网络的假设是什么？为何使用 Layer
Norm 而不是 Batch Norm？Transformer 是否有其它更好的 Normalization 的实现？

-- 3 of 72 --

Layer Normalization 的假设： Layer Normalization 假设在每个层中的输入特征都是独立同分布

### 片段 7

tion 的实现？

-- 3 of 72 --

Layer Normalization 的假设： Layer Normalization 假设在每个层中的输入特征都是独立同分布
的。换句话说，对于每个神经元的输入，它们的分布应该相似且稳定，因此可以通过对每个神经元的
输入进行归一化来加快网络的训练收敛速度。
为何使用 Layer Norm 而不是 Batch Norm： 在 Transformer 中，由于每个位置的输入都是独立处
理的，而不是像卷积神经网络中的批处理（Batch Processing），因此 Batch Normalization 的假
设并不适用。此外，由于 Transformer 中涉及到不同位置的注意力计算，批处理的概念不再适用。
相比之下，Layer Normalization 更适合 Transformer，因为它在每个位置的特征维度上进行归一化，
而不是在批处理的维度上进行归一化。
Transformer 是否有更好的 Normalization 实现： 除了 Layer Normalization，还有一些变体和改

### 片段 8

一化，
而不是在批处理的维度上进行归一化。
Transformer 是否有更好的 Normalization 实现： 除了 Layer Normalization，还有一些变体和改
进的归一化技术被提出用于 Transformer 模型，如 Instance Normalization、Group Normalization
等。这些方法有时会根据具体的任务和实验结果进行选择。另外，一些新的归一化技术也在不断地被
研究和提出，以进一步改善模型的性能和训练效果。
总 的 来 说 ， Layer Normalization 在 Transformer 中 是 一 个 比 较 合 适 的 选 择 ， 因 为 它 更 符 合
Transformer 模型的独立同分布的假设，并且相对于 Batch Normalization 更适用于处理独立的位
置特征。
7，Transformer 中的神经网络为何能够很好的表示信息？
Transformer 中的神经网络能够很好地表示信息的原因可以归结为以下几点：

### 片段 9

更适用于处理独立的位
置特征。
7，Transformer 中的神经网络为何能够很好的表示信息？
Transformer 中的神经网络能够很好地表示信息的原因可以归结为以下几点：
Self-Attention 机制： Transformer 引入了 Self-Attention 机制，使得模型能够在计算时同时考虑
输入序列中不同位置之间的依赖关系。通过自注意力机制，模型可以根据输入序列中每个位置的重要
性来动态调整对应位置的表示，从而更好地捕捉输入序列中的长距离依赖关系和语义信息。
多头注意力机制： Transformer 中的注意力机制被扩展为多头注意力机制，允许模型在不同的注意
力头中学习到不同的表示。这样可以提高模型对输入序列的多样性建模能力，使得模型能够更好地理
解不同层次和方面的语义信息。

-- 4 of 72 --

位置编码： Transformer 使用位置编码来将位置信息融入输入序列的表示中，从而使模型能够理解
输入序列中词语的位置顺序。位置编码允许模型在表示时区分不同位置的词语，有助于模型更好地捕
捉到序列中的顺序信息。

### 片段 10

使用位置编码来将位置信息融入输入序列的表示中，从而使模型能够理解
输入序列中词语的位置顺序。位置编码允许模型在表示时区分不同位置的词语，有助于模型更好地捕
捉到序列中的顺序信息。
残差连接和层归一化： Transformer 中的每个子层（如 Multi-Head Attention 和 Feedforward 层）
都使用了残差连接和层归一化来缓解梯度消失和梯度爆炸问题，使得模型更容易训练并且能够更好地
利用深层网络结构。
更强大的表示能力： Transformer 模型由多个 Encoder 和 Decoder 堆叠而成，每个 Encoder 和
Decoder 都包含多个层，每个层中又包含了多个子层。这种深层结构使得 Transformer 具有更强大
的表示能力，能够学习到复杂的输入序列表示，并且适用于各种自然语言处理任务。
8，请从数据的角度分析 Transformer 中的 Decoder 和 Encoder 的依存关系
Encoder 的依存关系：
输入数据：Encoder 的输入数据通常是一个词嵌入序列，代表输入语言中的单词或标记。

### 片段 11

rmer 中的 Decoder 和 Encoder 的依存关系
Encoder 的依存关系：
输入数据：Encoder 的输入数据通常是一个词嵌入序列，代表输入语言中的单词或标记。
处理过程：Encoder 将输入数据作为词嵌入序列，经过多层的自注意力机制（Self-Attention）和前
馈神经网络（Feedforward Neural Network）处理，逐步提取输入序列的特征表示。
输出数据：Encoder 的输出是一个经过编码的特征表示序列，其中每个位置包含了对应输入序列的
信息。
Decoder 的依存关系：
输入数据：Decoder 的输入数据通常是一个目标语言的词嵌入序列，或者是一个起始标记（如
<start>）。
处理过程：Decoder 在每个时间步都生成一个输出词，通过自注意力机制和编码器-解码器注意力机
制（Encoder-Decoder Attention）来对输入序列和当前时间步生成的部分序列进行建模。Decoder
会逐步生成目标语言的输出序列，直到生成特殊的结束标记（如<end>）。
输出数据：Decoder 的输出是一个目标语言的词嵌入序列，或者是一个目标语言的单词序列，代表

### 片段 12

ecoder
会逐步生成目标语言的输出序列，直到生成特殊的结束标记（如<end>）。
输出数据：Decoder 的输出是一个目标语言的词嵌入序列，或者是一个目标语言的单词序列，代表
了模型对输入序列的翻译或生成结果。

-- 5 of 72 --

Encoder 和 Decoder 之间的依存关系：
Encoder-Decoder Attention：在 Decoder 的每个时间步，Decoder 会使用 Encoder-Decoder
Attention 来关注输入序列的不同位置，并结合当前时间步生成的部分序列来生成下一个输出词。这
种注意力机制允许 Decoder 根据输入序列的特征来动态调整生成输出序列的策略。
最终输出：Encoder 和 Decoder 之间的依存关系体现在最终的输出结果中，Decoder 的输出受到了
Encoder 提取的特征表示的影响，以此来保留输入序列的信息并生成相应的输出序列。
总的来说，Encoder 和 Decoder 之间的依存关系体现在数据的流动和信息的交互中。Encoder 通过

## 使用建议

- 这些内容来自授权公开 PDF 的文本抽取结果，网页端会基于同一份静态索引做关键词检索。
- 面试复习时建议先用网页 PDF 原文检索定位题目，再回到主 notes 学系统化答案。
- 如果片段出现排版噪声，以原 PDF 语义为准，并优先整理成自己的回答模板。
