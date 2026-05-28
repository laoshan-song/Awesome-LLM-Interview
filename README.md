<div align="center">

# 🧠 Awesome LLM Interview

**大模型面试知识点精华整理 · 每日持续更新**

[![GitHub stars](https://img.shields.io/github/stars/laoshan-song/Awesome-LLM-Interview?style=social)](https://github.com/laoshan-song/Awesome-LLM-Interview)
[![GitHub forks](https://img.shields.io/github/forks/laoshan-song/Awesome-LLM-Interview?style=social)](https://github.com/laoshan-song/Awesome-LLM-Interview)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/laoshan-song/Awesome-LLM-Interview/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![持续更新](https://img.shields.io/badge/每日更新-进行中-brightgreen.svg)]()

</div>

---

## 这个仓库是什么？

**一句话**：你备战大模型面试时，希望有人帮你把所有核心知识点整理清楚——这个仓库就是干这个的。

每篇笔记包含：**面试高频考点 + 核心原理 + 原始论文 + 视频讲解**。

> 如果你觉得有用，点个 ⭐ Star 是对我最大的鼓励！

---

## 📚 知识点目录

### 🔤 一、基础架构

| 编号 | 主题 | 最近更新 |
|------|------|----------|
| 01 | [LLM 核心名词解释](./notes/01_基础架构/01_名词解释.md) | 补全 Token / Attention / KV Cache 等 30+ 核心术语 |
| 02 | [分词算法（BPE / WordPiece / SentencePiece）](./notes/01_基础架构/02_分词算法.md) | 添加 Karpathy 视频 + 3 篇原始论文链接 |
| 03 | [Transformer 架构详解](./notes/01_基础架构/03_Transformer架构.md) | 添加 3Blue1Brown 可视化视频 + 原版论文 |
| 04 | [位置编码（RoPE / ALiBi / sinusoidal）](./notes/01_基础架构/04_位置编码.md) | 补充 RoPE / ALiBi 论文 + 外推方案对比 |
| 05 | [主流模型架构对比（LLaMA / Qwen / DeepSeek）](./notes/01_基础架构/05_主流模型架构对比.md) | 新增：MLA、RMSNorm、SwiGLU 等架构细节 |

### ⚙️ 二、训练与对齐

| 编号 | 主题 | 最近更新 |
|------|------|----------|
| 06 | [预训练 vs 微调 vs RLHF](./notes/02_训练与对齐/05_预训练与微调.md) | 补充 InstructGPT / LIMA 论文 + 三阶段流程 |
| 07 | [SFT 有监督微调](./notes/02_训练与对齐/06_SFT.md) | 补充数据质量分析 + loss 计算细节 |
| 08 | [RLHF / DPO / PPO 对比](./notes/02_训练与对齐/07_RLHF_DPO_PPO.md) | 添加李沐精读视频 + DPO 完整推导 |
| 09 | [LoRA 及参数高效微调（PEFT）](./notes/02_训练与对齐/08_LoRA与PEFT.md) | 添加论文精读视频 + QLoRA 细节 |
| 10 | [预训练数据处理](./notes/02_训练与对齐/09_预训练数据处理.md) | 新增：数据清洗、去重、配比策略 |

### 🚀 三、推理与优化

| 编号 | 主题 | 最近更新 |
|------|------|----------|
| 11 | [KV Cache 原理与优化](./notes/03_推理与优化/09_KV_Cache.md) | 补充显存公式 + GQA / PagedAttention |
| 12 | [量化（INT8 / INT4 / GPTQ / AWQ）](./notes/03_推理与优化/10_量化.md) | 补充 GPTQ / AWQ / SmoothQuant 论文 |
| 13 | [解码策略（Greedy / Beam / Sampling）](./notes/03_推理与优化/11_解码策略.md) | 补充 Top-p 论文 + 场景使用建议 |
| 14 | [推理加速（Flash Attention / vLLM / 投机采样）](./notes/03_推理与优化/12_推理加速.md) | 补充 Flash Attention / 投机采样 4 篇论文 |

### 🖥️ 四、分布式训练

| 编号 | 主题 | 最近更新 |
|------|------|----------|
| 15 | [数据并行与模型并行](./notes/04_分布式训练/01_数据并行与模型并行.md) | 新增：ZeRO 三阶段、张量/流水线并行对比 |
| 16 | [显存优化技巧](./notes/04_分布式训练/02_显存优化技巧.md) | 新增：梯度检查点、混合精度、显存占用公式 |

### 🔬 五、前沿专题

| 编号 | 主题 | 最近更新 |
|------|------|----------|
| 17 | [MoE 混合专家模型](./notes/05_前沿专题/13_MoE.md) | 补充 Mixtral / Switch Transformer 论文 |
| 18 | [RAG 检索增强生成](./notes/05_前沿专题/14_RAG.md) | 添加 IBM 视频 + Self-RAG 论文 |
| 19 | [Agent 与工具调用](./notes/05_前沿专题/15_Agent.md) | 补充 ReAct / Toolformer 论文 |
| 20 | [Prompt Engineering](./notes/05_前沿专题/16_Prompt_Engineering.md) | 新增：CoT / ToT / Self-Consistency / 提示注入防御 |
| 21 | [大模型幻觉与评估](./notes/05_前沿专题/17_大模型幻觉与评估.md) | 新增：幻觉分类、MMLU/HumanEval、LLM-as-Judge |

---

## 🤝 欢迎一起完善

学一个人的笔记，不如一群人共同维护一份高质量知识库。

你可以贡献：
- 📝 **完善某个知识点**的讲解（更清晰的例子、更准确的描述）
- 🎬 **推荐优质视频**（B 站 / YouTube 都欢迎）
- 📄 **补充新的论文**（最新进展、重要综述）
- 🌟 **新增知识点**（多模态、长文本、代码大模型……）

```bash
# Fork → 新建分支 → 修改 → PR
git checkout -b feat/your-topic
git commit -m "补充：xxx 知识点 / 添加：xxx 视频"
git push origin feat/your-topic
```

---

## 🗓️ 更新日志

| 更新内容 |
|----------|
| 🎉 初始化仓库，完成 LLM 核心名词解释 |
| 📚 补全 15 篇核心知识点（基础 / 训练 / 推理 / 工程） |
| 📄 为所有知识点补充原始论文 arxiv 链接 |
| 🎬 添加 Karpathy / 3Blue1Brown / 李沐等优质视频资源 |
| 🗂️ 重构目录：按主题分为 5 大类，新增分布式训练、Prompt Engineering、幻觉评估等前沿专题 |

---

<div align="center">

**⭐ Star 一下，下次面试前不慌 ⭐**

*一个人走得快，一群人走得远。欢迎 PR 共建！*

</div>
