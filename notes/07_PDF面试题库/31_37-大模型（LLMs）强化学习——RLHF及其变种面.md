# 37-大模型（LLMs）强化学习——RLHF及其变种面

> 来源 PDF：`200页AI大模型面试高频必刷题（附详解）/37-大模型（LLMs）强化学习——RLHF及其变种面.pdf`  
> 主题：训练 / 微调  
> 页数：14  
> 字符数：8903  
> 索引片段数：22

## 摘要

大模型（LLMs）强化学习——RLHF及其变种面 来自： AiGC面试宝典 宁静致远 2024年01月27日 20:47 一、介绍一下 LLM的经典预训练Pipeline？ • 大模型（LLMs）强化学习——RLHF及其变种面 • 一、介绍一下 LLM的经典预训练Pipeline？ • 二、预训练（Pre-training）篇 • 2.1 具体介绍一下 预训练（Pre-training）？ • 三、有监督微调（Supervised Tinetuning）篇 • 3.1 具体介绍一下 有监督微调（Supervised

## 代表性原文片段

### 片段 1

大模型（LLMs）强化学习——RLHF及其变种面
来自： AiGC面试宝典
宁静致远 2024年01月27日 20:47
一、介绍一下 LLM的经典预训练Pipeline？
• 大模型（LLMs）强化学习——RLHF及其变种面
• 一、介绍一下 LLM的经典预训练Pipeline？
• 二、预训练（Pre-training）篇
• 2.1 具体介绍一下 预训练（Pre-training）？
• 三、有监督微调（Supervised Tinetuning）篇
• 3.1 具体介绍一下 有监督微调（Supervised Tinetuning）？
• 3.2 有监督微调（Supervised Tinetuning）的训练数据格式是什么样？
• 3.3 预训练（Pre-training） vs 有监督微调（Supervised Tinetuning）区别？
• 四、对齐（Alignment）篇
• 4.1 简单介绍一下 对齐（Alignment）？
• 五、Reinforcement Learning with Human Feedback (RLHF)篇
• 5.1 简单介绍一下 RLHF 流程？

### 片段 2

齐（Alignment）？
• 五、Reinforcement Learning with Human Feedback (RLHF)篇
• 5.1 简单介绍一下 RLHF 流程？
• 5.2 如何在在预训练好的模型上进行有监督微调？
• 5.3 如何在有监督微调模型基础上创建一个RM模型？
• 5.4 如何基于RM模型使用PPO算法微调SFT模型？
• 5.5 instructGPT的原理，讲讲rlhf和reward？
• 六、LLaMA 2 的 RLHF 篇
• 6.1 介绍一下 LLaMA 2 的 RLHF？
• 6.2 LLaMA 2 中 Margin Loss 的 实现逻辑？
• 6.3 LLaMA 2 中 两个RM模型 的 实现逻辑？
• 6.4 LLaMA 2 中 拒绝采样 逻辑？
• 七、 RLHF 替代方案篇
• 7.1 为什么需要 RLHF 替代方案？
• 7.2 RLHF 有哪些替代方案？
• 替代方案 1：Constitutional AI: Harmlessness from AI Feedback

### 片段 3

要 RLHF 替代方案？
• 7.2 RLHF 有哪些替代方案？
• 替代方案 1：Constitutional AI: Harmlessness from AI Feedback
• 替代方案 2：The Wisdom of Hindsight Makes Language Models Better Instruction
Followers
• 替代方案 3：Direct Preference Optimization: Your Language Model is Secretly a
Reward Model
• 替代方案 4：Reinforced Self-Training (ReST) for Language Modeling
• 替代方案 5：RLAIF: Scaling Reinforcement Learning from Human Feedback with AI
Feedback
• 八、 RLHF 实践篇
• 8.1 RLHF 训练过程，怎么选取最优 checkpoint？
• 参考
扫码加
查看更多

-- 1 of 14 --

### 片段 4

AI
Feedback
• 八、 RLHF 实践篇
• 8.1 RLHF 训练过程，怎么选取最优 checkpoint？
• 参考
扫码加
查看更多

-- 1 of 14 --

目前基于Transformer decoder的LLM，比如ChatGPT、LLaMA、baichuan等，通常都会有基于预训练的base模
型和在base模型至少使用RLHF微调的Chat模型，Chat模型的训练一般都包括如下三个步骤：预训练，有监督微
调和对齐。
二、预训练（Pre-training）篇
2.1 具体介绍一下 预训练（Pre-training）？
预训练（Pre-training）：利用数十亿到数万亿个token的庞大文本语料库 对模型继续 预训练，使 模型 能够 根据
提供的文本来预测「下一个单词」。
三、有监督微调（Supervised Tinetuning）篇
3.1 具体介绍一下 有监督微调（Supervised Tinetuning）？
有监督微调（Supervised Tinetuning）:虽然 SFT 训练目标和 预训练（Pre-training）类似，也是 需要模型 预测

### 片段 5

ised Tinetuning）？
有监督微调（Supervised Tinetuning）:虽然 SFT 训练目标和 预训练（Pre-training）类似，也是 需要模型 预测
「下一个单词」，但是需要人工标注的指令数据集，其中模型的输入是一个指令（根据任务的不同，也可能包含
一段输入文本），输出为模型的预期回复内容。
1. 在预训练阶段，模型会从大量无标注文本数据集中学习通用知识；
2. 使用「有监督微调」（SFT）优化模型以更好地遵守特定指令；
3. 使用对齐技术使LLM可以更有用且更安全地响应用户提示。

-- 2 of 14 --

3.2 有监督微调（Supervised Tinetuning）的训练数据格式是什么样？
Instruction: "Write a limerick about a pelican."
指令：“写一首关于鹈鹕的打油诗。“
Output: "There once was a pelican so fine..."
输出：“从前有一只鹈鹕很好...“

### 片段 6

elican."
指令：“写一首关于鹈鹕的打油诗。“
Output: "There once was a pelican so fine..."
输出：“从前有一只鹈鹕很好...“
模型会把“Write a limerick about a pelican”作为输入，逐个token进行预测，输出“There once was a pelican so
fine...”
3.3 预训练（Pre-training） vs 有监督微调（Supervised Tinetuning）区别？
四、对齐（Alignment）篇
4.1 简单介绍一下 对齐（Alignment）？
对齐（Alignment）：通过微调的方式，将语言模型与人类的偏好、价值观进行对齐，这也是RLHF机制发挥的地
方。
• 相同点：
• 训练目标相同：模型需要根据提供的文本来预测「下一个单词」；
• 不同点：
• 训练数据量不同：有监督微调（Supervised Tinetuning）需要训练数据量比 预训练（Pre-training）
小很多；

### 片段 7

文本来预测「下一个单词」；
• 不同点：
• 训练数据量不同：有监督微调（Supervised Tinetuning）需要训练数据量比 预训练（Pre-training）
小很多；
• 训练数据格式不同：有监督微调（Supervised Tinetuning）需要人工标注的训练数据，预训练（Pre-
training） 不需要；

-- 3 of 14 --

五、Reinforcement Learning with Human Feedback (RLHF)篇
5.1 简单介绍一下 RLHF 流程？
5.2 如何在在预训练好的模型上进行有监督微调？
先收集一个Prompts集合，并要求标注人员写出高质量的回复，然后使用该数据集以监督的方式微调预训练的基
础模型。
5.3 如何在有监督微调模型基础上创建一个RM模型？
对于每个Prompt，要求有监督微调后的LLM生成四到九个回复，再由标注人员根据个人偏好对所有回复进行排
序。虽然排序过程很耗时，但工作量还是比第一步的有监督数据集构建要少一些。
1. 在预训练好的模型上进行「有监督微调」（SFT）；

### 片段 8

九个回复，再由标注人员根据个人偏好对所有回复进行排
序。虽然排序过程很耗时，但工作量还是比第一步的有监督数据集构建要少一些。
1. 在预训练好的模型上进行「有监督微调」（SFT）；
2. 在有监督微调模型基础上创建一个reward model（RM）模型；
3. 基于RM模型使用PPO算法微调SFT模型；

-- 4 of 14 --

在处理排序数据时，使用了一个奖励模型RM，RM来自RLHF第一步的「有监督微调语言模型」（SFT），SFT
的输出通过一个回归层（单个输出节点）转换为奖励分数，即可称为RM模型。
5.4 如何基于RM模型使用PPO算法微调SFT模型？
基于RM模型使用proximal policy optimization (PPO)算法微调SFT模型
5.5 instructGPT的原理，讲讲rlhf和reward？
instructGPT是一种基于强化学习的文本生成模型，其核心原理涉及两个概念：RLHF（Reinforcement Learning
from Human Feedback）和reward shaping（奖励塑造）。

### 片段 9

的文本生成模型，其核心原理涉及两个概念：RLHF（Reinforcement Learning
from Human Feedback）和reward shaping（奖励塑造）。
通过RLHF和reward shaping的结合，instructGPT能够通过人类评估者的反馈指导模型的生成过程，并逐步提升
生成文本的质量和一致性。
• RLHF：在训练instructGPT时，首先使用有人类生成的示例对模型进行预训练。然后，通过与人类评估者进
行交互，收集评估结果，以创建一个用于强化学习的数据集。该数据集包含了人类评估者对生成结果的评分
或反馈，用于指导模型的强化学习训练。
• Reward shaping：为了更好地引导模型的训练，reward shaping用于调整模型的奖励信号。通过将人类评估
者的反馈与模型生成的文本进行比较，可以计算出一个差异度量，用作奖励信号的一部分。这样，模型可以
根据这个奖励信号进行训练，并进行强化学习的训练。模型根据当前的状态（对话历史）生成文本，并通过
奖励信号来评估生成文本的质量。模型的目标是最大化预期累积奖励，从而生成更高质量的文本。

-- 5 of 14 --

### 片段 10

化学习的训练。模型根据当前的状态（对话历史）生成文本，并通过
奖励信号来评估生成文本的质量。模型的目标是最大化预期累积奖励，从而生成更高质量的文本。

-- 5 of 14 --

六、LLaMA 2 的 RLHF 篇
6.1 介绍一下 LLaMA 2 的 RLHF？
Llama-2-chat在第一步RLHF微调上使用相同的指令数据，但在第二步使用了两个奖励模型；通过多个阶段的不
断进化，奖励模型也会根据Llama-2-chat模型出现的错误进行更新；并且增加了拒绝采样（rejection
sampling）步骤。
6.2 LLaMA 2 中 Margin Loss 的 实现逻辑？
eg：四个回复的排序结果为A<C< D<B，那么就可以得到六个对比结果：A < C，A < D ，A < B，C < D，C <
B，D < B
在排序训练时中，Llama 2相比InstructGPT增加了边际损失：
其中，rθ（x，y）是提示x和生成的回复y的标量分数输出; θ为模型权重; σ是将层输出转换为范围
从0到1的分数的逻辑S形函数; yc是由标注人员选择的更优回复; yr是较差的回复。m(r)可以调节

### 片段 11

是提示x和生成的回复y的标量分数输出; θ为模型权重; σ是将层输出转换为范围
从0到1的分数的逻辑S形函数; yc是由标注人员选择的更优回复; yr是较差的回复。m(r)可以调节
两个回复之间的差值，如果对比结果为「显著更好」，则会增加梯度值，加快更新速度。
6.3 LLaMA 2 中 两个RM模型 的 实现逻辑？
Llama 2中的两个奖励模型：
用于模型优化的最终奖励函数会将两个分数进行线性组合。
• 标准InstructGPT 中 RLHF PPO方法 思路：对同一个提示下的4-9个模型输出并进行排序。
• Llama 2 的 Margin Loss：每次只能看到两个（而非4-9个）回复并进行对比，但新增了一个边际（margin）
标签，对比结果可以为「显著更好」（significantly better）和「好的不明显」（negligibly better）
• 侧重「有用性」（helpfulness）
• 「安全性」（safety）

-- 6 of 14 --

6.4 LLaMA 2 中 拒绝采样 逻辑？

### 片段 12

ibly better）
• 侧重「有用性」（helpfulness）
• 「安全性」（safety）

-- 6 of 14 --

6.4 LLaMA 2 中 拒绝采样 逻辑？
Llama 2 使用了一个训练流水线，同时使用PPO和拒绝采样算法，迭代地产生多个RLHF模型（从RLHF-V1到
RLHF-V5），模型在拒绝采样时会得到K个输出，并使用最高奖励的输出更新梯度，而PPO每次只基于单样本进
行更新。
在监督微调的初始阶段之后，模型只使用拒绝采样进行训练，然后再结合拒绝采样和PPO。
七、 RLHF 替代方案篇
7.1 为什么需要 RLHF 替代方案？
虽然 RLHF在InstructGPT和Llama 2论文中被证明是有效的，但是RLHF的过程是比较复杂的。

-- 7 of 14 --

7.2 RLHF 有哪些替代方案？
替代方案 1：Constitutional AI: Harmlessness from AI Feedback
论文名称：Constitutional AI: Harmlessness from AI Feedback

## 使用建议

- 这些内容来自授权公开 PDF 的文本抽取结果，网页端会基于同一份静态索引做关键词检索。
- 面试复习时建议先用网页 PDF 原文检索定位题目，再回到主 notes 学系统化答案。
- 如果片段出现排版噪声，以原 PDF 语义为准，并优先整理成自己的回答模板。
