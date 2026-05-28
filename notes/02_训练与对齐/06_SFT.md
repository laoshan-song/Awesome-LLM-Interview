# SFT 有监督微调

## 面试高频考点
- SFT 的数据格式是什么？为什么只对 Assistant 部分计算 loss？
- SFT 和预训练的本质区别？
- 如何防止 SFT 导致的灾难性遗忘？
- 数据质量 vs 数量？LIMA 论文的核心结论？
- SFT 数据如何构造和清洗？

---

## 一、SFT 是什么？

Supervised Fine-Tuning（有监督微调），在预训练模型的基础上，使用**人工标注的高质量指令-回答对**继续训练，使模型从"预测下一个 token"转变为"遵循指令完成任务"。

```
预训练模型：
  输入："今天天气真"
  输出："好"  ← 只是预测下一个词，不会"对话"

SFT 后：
  输入："请用 JSON 格式返回今天的天气预报"
  输出：'{"city":"北京","temp":25,"weather":"晴"}'  ← 理解指令并执行
```

SFT 是让模型"听懂人话"的关键一步，是从原始 LLM 到可用助手的必经之路。

---

## 二、数据格式详解

### Chat Template（对话模板）

现代模型（LLaMA、Qwen、DeepSeek）使用标准化的对话模板：

```
<|begin_of_text|>
<|system|>
你是一个专业、准确、有帮助的AI助手。
<|user|>
请用三句话解释什么是 Transformer
<|assistant|>
Transformer 是一种基于自注意力机制的神经网络架构...
<|end_of_text|>
```

### Loss Masking——为什么只对 Assistant 部分计算 loss？

这是 SFT 最关键的设计选择之一：

```
Token 序列：
[<system>] [你是一个...] [<user>] [请解释...] [<assistant>] [Transformer是...] [<eot>]
     ↓           ↓           ↓         ↓            ↓              ↓            ↓
Loss: ✗          ✗           ✗         ✗            ✓              ✓            ✓

只计算 Assistant 回复部分的交叉熵损失
System Prompt 和 User 输入部分不参与 loss 计算
```

**原因**：
1. 训练目标是"学会怎么回答"，不是"学会怎么提问"
2. 如果对 User 输入也计算 loss，模型会学偏——记住具体的用户问题而非学会回答
3. 保证模型在推理时能处理任意形式的问题，而不是只对训练中见过的 prompt 格式有效

### 数据格式的最佳实践

| 要素 | 建议 |
|------|------|
| 指令多样性 | 覆盖问答、写作、推理、代码、翻译、摘要等不同类型 |
| 难度分布 | 包含简单和复杂任务，防止模型"挑软柿子" |
| 长度分布 | 短回复和长回复混合，模型才能学会根据需求控制长度 |
| 多轮对话 | 多轮对话数据让模型学会跟踪上下文和指代 |
| System Prompt | 不同 system prompt 增强角色适应能力 |
| 拒绝/边界 | 包含合理的拒答示例（"我不知道"、"这超出了我的知识范围"） |

---

## 三、SFT vs 预训练的本质区别

| 维度 | 预训练 | SFT |
|------|--------|-----|
| 数据量 | 万亿 Token 级别 | 万~十万条（高质量） |
| 数据来源 | 互联网爬取（噪声大） | 人工标注/LLM 生成+人工校验 |
| 学习目标 | Next Token Prediction | 指令遵循 |
| Loss 计算 | 全序列所有 token | 仅 Assistant 部分（Loss Masking） |
| 学习率 | 较大（1e-4 ~ 3e-4） | 较小（1e-5 ~ 5e-5） |
| Epoch 数 | 1 epoch（数据量足够） | 1-3 epochs |
| 核心挑战 | 数据清洗、配比、去重 | 数据质量、多样性、防止遗忘 |
| 产出 | Base Model | Chat/Instruct Model |

---

## 四、数据质量 vs 数量：LIMA 的启示

### LIMA（Less Is More for Alignment, 2023）

**核心发现**：仅用 **1000 条精心挑选的高质量 SFT 数据**，就能让 65B 模型达到接近 GPT-4 级别的对齐效果（人类评估中 43% vs GPT-4 的 58%）。

```
LIMA 1000 条数据 vs Alpaca 52000 条数据：

LIMA (1000条高质量)：
  人类评估胜率：43%（与 GPT-4 对比）
  数据来源：社区精选 + 人工编写

Alpaca (52000条 LLM生成)：
  人类评估胜率：显著低于 LIMA
  数据来源：GPT-3.5 自动生成（含大量模板化、低质量数据）

结论：100 条高质量数据 > 10000 条低质量数据
```

### 数据质量的关键维度

```
什么是高质量 SFT 数据？

✅ 好数据：
  - 指令明确、具体、可执行
  - 回复准确、完整、格式规范
  - 推理步骤清晰（CoT 风格）
  - 承认不确定性和知识边界
  - 多轮对话中追踪上下文

❌ 差数据：
  - 指令模糊（"写点什么"）
  - 回复过短/过长不符合预期
  - 事实错误
  - 格式不一致（同一类任务有时 JSON 有时纯文本）
  - 模板化（"当然！让我来帮你..." 每句都重复）
```

---

## 五、灾难性遗忘与缓解

### 什么是灾难性遗忘？

SFT 使模型过度适应微调数据的分布，导致在未覆盖任务上的能力下降：

```
SFT 前的模型：
  代码能力: ████████ (优秀)
  数学能力: ████████ (优秀)
  通用对话: ██░░░░░░ (差)

仅用对话数据 SFT 后：
  代码能力: ██░░░░░░ (严重退化！)
  数学能力: ███░░░░░ (退化！)
  通用对话: ████████ (提升)

这就是灾难性遗忘：学了一项，忘了其他的
```

### 缓解方案

| 方法 | 原理 | 效果 |
|------|------|------|
| **混合预训练数据** | SFT 数据中混入 5-20% 原始预训练语料 | 保持通用能力 |
| **小学习率** | 减少每次更新的幅度，降低对原始权重的破坏 | 牺牲收敛速度换稳定性 |
| **LoRA 微调** | 只训练低秩附加矩阵，冻结原始权重 | 结构上防止遗忘 |
| **数据多样性** | 确保 SFT 数据覆盖多种任务类型 | 防止分布偏移 |
| **渐进式微调** | 先简单任务后复杂任务，逐步增加难度 | 平滑过渡 |
| **Replay Buffer** | 定期回放预训练数据 | 保持旧知识 |

---

## 六、SFT 数据的构造方法

### Self-Instruct（自指令）

用强大的 LLM（如 GPT-4）自动生成指令数据：

```
1. Seed Tasks：人工编写 175 个种子任务
2. Instruction Generation：用 LLM 基于种子生成新指令
3. Classification：判断生成的任务是否有效
4. Response Generation：用 LLM 生成回复
5. Filtering：过滤低质量数据（长度、格式、Rouge-L 去重）

最终产出数万条 (指令, 回复) 对
```

### 数据蒸馏

从更强的模型的输出中学习：

```
Teacher Model（如 GPT-4 / DeepSeek-R1）→ 生成高质量回复
Student Model（如 LLaMA-7B） → 学习模仿 Teacher 的输出

优点：成本低、质量可控、可规模化
风险：学到 Teacher 的风格偏见、可能过拟合 Teacher 的错误模式
```

### Evo-Instruct（WizardLM）

从小模型逐步进化到更复杂的指令：

```
In-Breadth Evolution：扩展指令的主题和类型覆盖
In-Depth Evolution：增加指令的复杂度和条件约束
Elimination：过滤失败/低质演化结果

产出从简单到复杂的渐进式指令数据集
```

---

## 七、面试延伸

**Q：SFT 数据多样性为什么重要？**

> 如果只在代码数据上做 SFT，模型会失去通用对话、数学推理等能力。多样化的指令数据让模型学到的是"遵循任何指令"的元能力（meta-ability），而不是记住特定任务的回答。关键是让模型泛化到未见过的指令格式和任务类型。

**Q：如何评估 SFT 效果？**

> ① MT-Bench（多轮对话评测，GPT-4 打分 1-10）；② AlpacaEval（A/B 测试，计算对其他模型的胜率）；③ 人工评估（找人对比评分，最可靠但成本高）；④ 领域专项评测（如代码 SFT 后用 HumanEval 评测，不只看对话能力）。自动化指标（BLEU/ROUGE）对生成任务参考价值有限，LLM-as-Judge 是目前主流的自动化方案。

**Q：SFT 要做几个 Epoch？过拟合风险大吗？**

> 通常 1-3 epochs。SFT 数据量远小于预训练，过拟合风险确实存在。监控验证集 loss：如果连续上升而训练 loss 还在下降，就是过拟合了。实践中 1-2 epochs 对大多数场景足够。数据量越多（10万+），可以做 2-3 epochs；数据量少（千条级别），1 epoch 即可，否则容易灾难性遗忘。

**Q：Multi-turn SFT 有什么特殊处理？**

> 多轮对话数据的每轮都可能需要不同的处理：① 每轮单独作为一条训练样本（拆分多轮为多个单轮）；② 整段多轮作为一条样本（保留上下文连续性）。实践中常用方案 ②，但将 loss 只计算在最后的 Assistant 回复上（忽略中间轮），或使用 Packing 技巧把多轮对话的多个 Assistant 片段拼接计算 loss。

---

## 原始论文

| 论文 | 链接 |
|------|------|
| LIMA: Less Is More for Alignment (Zhou et al., NeurIPS 2023) | [arxiv.org/abs/2305.11206](https://arxiv.org/abs/2305.11206) |
| Self-Instruct: Aligning LM with Self Generated Instructions (Wang et al., ACL 2023) | [arxiv.org/abs/2212.10560](https://arxiv.org/abs/2212.10560) |
| WizardLM: Empowering LLMs to Follow Complex Instructions (Xu et al., 2023) | [arxiv.org/abs/2304.12244](https://arxiv.org/abs/2304.12244) |
| Training language models to follow instructions (InstructGPT) (Ouyang et al., NeurIPS 2022) | [arxiv.org/abs/2203.02155](https://arxiv.org/abs/2203.02155) |
| Orca: Progressive Learning from Complex Explanation Traces (Mukherjee et al., 2023) | [arxiv.org/abs/2306.02707](https://arxiv.org/abs/2306.02707) |

## 延伸阅读与视频

| 平台 | 标题 | 说明 |
|------|------|------|
| 📺 B站 | [大模型微调看这个视频就够了 SFT NEFTune](https://www.bilibili.com/video/BV1Cf421p71Q/) | 5.7万播放，SFT全流程+NEFTune噪声增强技巧 |
| 📺 B站 | [20分钟带你快速弄懂SFT、RLHF、DPO](https://www.bilibili.com/video/BV1yMNteMEYv/) | 从定义到适用边界全流程解析 |
| 📺 B站 | [SFT一行一行代码实现并跑通（动手学大模型12.1）](https://www.bilibili.com/video/BV1JZHzerEb1/) | 代码级实现 SFT，适合动手学习 |
