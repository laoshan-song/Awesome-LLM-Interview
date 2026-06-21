# 2-Layer normalization 篇

> 来源 PDF：`200页AI大模型面试高频必刷题（附详解）/2-Layer normalization 篇.pdf`  
> 主题：Transformer / 基础架构  
> 页数：3  
> 字符数：1104  
> 索引片段数：3

## 摘要

Layer normalization 篇 来自： AiGC面试宝典 宁静致远 2023年09月29日 12:37 Layer normalization-方法篇 一、Layer Norm 篇 1.1 Layer Norm 的计算公式写一下？ 二、RMS Norm 篇 （均方根 Norm） 2.1 RMS Norm 的计算公式写一下？ 2.2 RMS Norm 相比于 Layer Norm 有什么特点？ RMS Norm 简化了 Layer Norm ，去除掉计算均值进行平移的部分。 对比LN，RMS Norm的计

## 代表性原文片段

### 片段 1

Layer normalization 篇
来自： AiGC面试宝典
宁静致远 2023年09月29日 12:37
Layer normalization-方法篇
一、Layer Norm 篇
1.1 Layer Norm 的计算公式写一下？
二、RMS Norm 篇 （均方根 Norm）
2.1 RMS Norm 的计算公式写一下？
2.2 RMS Norm 相比于 Layer Norm 有什么特点？
RMS Norm 简化了 Layer Norm ，去除掉计算均值进行平移的部分。
对比LN，RMS Norm的计算速度更快。效果基本相当，甚至略有提升。
三、Deep Norm 篇
3.1 Deep Norm 思路？
Deep Norm方法在执行Layer Norm之前，up-scale了残差连接 (alpha>1)；另外，在初始化阶段down-scale了模
型参数(beta<1)。
3.2 写一下 Deep Norm 代码实现？
Deep Norm 有什么优点？
扫码加
查看更多

-- 1 of 3 --

Deep Norm可以缓解爆炸式模型更新的问题，把模型更新限制在常数，使得模型训练过程更稳定。

### 片段 2

？
Deep Norm 有什么优点？
扫码加
查看更多

-- 1 of 3 --

Deep Norm可以缓解爆炸式模型更新的问题，把模型更新限制在常数，使得模型训练过程更稳定。
Layer normalization-位置篇
1 LN 在 LLMs 中的不同位置 有什么区别么？如果有，能介绍一下区别么？
回答：有，LN 在 LLMs 位置有以下几种：
1. Post LN：
a. 位置：layer norm在残差链接之后
b. 缺点：Post LN 在深层的梯度范式逐渐增大，导致使用post-LN的深层transformer容易出现训练不稳
定的问题
2. Pre-LN：
a. 位置：layer norm在残差链接中
b. 优点：相比于Post-LN，Pre LN 在深层的梯度范式近似相等，所以使用Pre-LN的深层transformer训
练更稳定，可以缓解训练不稳定问题
c. 缺点：相比于Post-LN，Pre-LN的模型效果略差
3. Sandwich-LN：
a. 位置：在pre-LN的基础上，额外插入了一个layer norm
b. 优点：Cogview用来避免值爆炸的问题

### 片段 3

，Pre-LN的模型效果略差
3. Sandwich-LN：
a. 位置：在pre-LN的基础上，额外插入了一个layer norm
b. 优点：Cogview用来避免值爆炸的问题
c. 缺点：训练不稳定，可能会导致训练崩溃。

-- 2 of 3 --

Layer normalization 对比篇
LLMs 各模型分别用了 哪种 Layer normalization？
BLOOM在embedding层后添加layer normalization，有利于提升训练稳定性:但可能会带来很大的性能损失
知识星球

-- 3 of 3 --

## 使用建议

- 这些内容来自授权公开 PDF 的文本抽取结果，网页端会基于同一份静态索引做关键词检索。
- 面试复习时建议先用网页 PDF 原文检索定位题目，再回到主 notes 学系统化答案。
- 如果片段出现排版噪声，以原 PDF 语义为准，并优先整理成自己的回答模板。
