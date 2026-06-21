# 27-适配器微调（Adapter-tuning）篇

> 来源 PDF：`200页AI大模型面试高频必刷题（附详解）/27-适配器微调（Adapter-tuning）篇.pdf`  
> 主题：Transformer / 基础架构  
> 页数：2  
> 字符数：1009  
> 索引片段数：3

## 摘要

适配器微调（Adapter-tuning）篇 来自： AiGC面试宝典 宁静致远 2023年09月18日 20:56 一、为什么 需要 适配器微调（Adapter-tuning）？ 二、适配器微调（Adapter-tuning）思路？ 三、 适配器微调（Adapter-tuning）特点是什么？ 四、AdapterFusion 思路 是什么？ 五、AdapterDrop 思路 是什么？ 六、AdapterDrop 特点 是什么？ 七、MAM Adapter 思路 是什么？ 八、MAM Adapter 特点 是什么？

## 代表性原文片段

### 片段 1

适配器微调（Adapter-tuning）篇
来自： AiGC面试宝典
宁静致远 2023年09月18日 20:56
一、为什么 需要 适配器微调（Adapter-tuning）？
二、适配器微调（Adapter-tuning）思路？
三、 适配器微调（Adapter-tuning）特点是什么？
四、AdapterFusion 思路 是什么？
五、AdapterDrop 思路 是什么？
六、AdapterDrop 特点 是什么？
七、MAM Adapter 思路 是什么？
八、MAM Adapter 特点 是什么？
1. 预训练模型参数量变多，在特定任务下进行全量微调即昂贵又耗时；
• 设计了Adapter结构（首先是一个down-project层将高维度特征映射到低维特征，然后过一个非线形层之后，
再用一个up-project结构将低维特征映射回原来的高维特征；同时也设计了skip-connection结构，确保了在最
差的情况下能够退化为identity），并将其嵌入Transformer的结构里面；
• 在训练时，固定住原来预训练模型的参数不变，只对新增的Adapter结构进行微调。同时为了保证训练的高效

### 片段 2

够退化为identity），并将其嵌入Transformer的结构里面；
• 在训练时，固定住原来预训练模型的参数不变，只对新增的Adapter结构进行微调。同时为了保证训练的高效
性（也就是尽可能少的引入更多参数）。
• 特点：
• 通过在Transformer层中嵌入Adapter结构，在推理时会额外增加推理时长。
• 思路：一种融合多任务信息的Adapter的变体，在 Adapter 的基础上进行优化，通过将学习过程分为两阶段来
提升下游任务表现。
• 思路：在不影响任务性能的情况下，对Adapter动态高效的移除，尽可能的减少模型的参数量，提高模型在反
向传播（训练）和正向传播（推理）时的效率。
• 特点：
• 通过从较低的 Transformer 层删除可变数量的Adaper来提升推理速度；
• 当对多个任务执行推理时，动态地减少了运行时的计算开销，并在很大程度上保持了任务性能。
• 思路：一种在 Adapter、Prefix Tuning 和 LoRA 之间建立联系的统一方法。最终的模型 MAM Adapter 是用于
FFN 的并行 Adapter 和 软提示的组合。
• 特点：

### 片段 3

ter、Prefix Tuning 和 LoRA 之间建立联系的统一方法。最终的模型 MAM Adapter 是用于
FFN 的并行 Adapter 和 软提示的组合。
• 特点：
• 整体上来说，最终的模型MAM Adapter效果会优于单个高效微调方法。
扫码加
查看更多

-- 1 of 2 --

知识星球

-- 2 of 2 --

## 使用建议

- 这些内容来自授权公开 PDF 的文本抽取结果，网页端会基于同一份静态索引做关键词检索。
- 面试复习时建议先用网页 PDF 原文检索定位题目，再回到主 notes 学系统化答案。
- 如果片段出现排版噪声，以原 PDF 语义为准，并优先整理成自己的回答模板。
