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

涵盖的方向：
- 🔤 **基础**：Tokenization、Transformer 架构、位置编码
- ⚙️ **训练**：预训练、SFT、RLHF、DPO、LoRA
- 🚀 **推理**：KV Cache、量化、解码策略、vLLM
- 🏗️ **工程**：MoE、RAG、Agent

每篇笔记包含：**面试高频考点 + 核心原理 + 原始论文 + 视频讲解**。

> 如果你觉得有用，点个 ⭐ Star 是对我最大的鼓励！

---

## 📚 知识点目录

### 🔤 基础篇

| 编号 | 主题 | 最近更新 |
|------|------|----------|
| 01 | [LLM 核心名词解释](./notes/01_名词解释.md) | 补全 Token / Attention / KV Cache 等 30+ 核心术语 |
| 02 | [分词算法（BPE / WordPiece / SentencePiece）](./notes/02_分词算法.md) | 添加 Karpathy 视频 + 3 篇原始论文链接 |
| 03 | [Transformer 架构详解](./notes/03_Transformer架构.md) | 添加 3Blue1Brown 可视化视频 + 原版论文 |
| 04 | [位置编码（RoPE / ALiBi / sinusoidal）](./notes/04_位置编码.md) | 补充 RoPE / ALiBi 论文 + 外推方案对比表 |

### ⚙️ 训练篇

| 编号 | 主题 | 最近更新 |
|------|------|----------|
| 05 | [预训练 vs 微调 vs RLHF](./notes/05_预训练与微调.md) | 补充 InstructGPT / LIMA 论文 + 三阶段流程图 |
| 06 | [SFT 有监督微调](./notes/06_SFT.md) | 补充数据质量 vs 数量分析 + loss 计算细节 |
| 07 | [RLHF / DPO / PPO 对比](./notes/07_RLHF_DPO_PPO.md) | 添加李沐 InstructGPT 精读视频 + DPO 推导 |
| 08 | [LoRA 及参数高效微调](./notes/08_LoRA与PEFT.md) | 添加 Yannic Kilcher 论文精读视频 + QLoRA |

### 🚀 推理与优化篇

| 编号 | 主题 | 最近更新 |
|------|------|----------|
| 09 | [KV Cache 原理与优化](./notes/09_KV_Cache.md) | 补充显存占用计算公式 + GQA / PagedAttention |
| 10 | [量化（INT8 / INT4 / GPTQ）](./notes/10_量化.md) | 补充 GPTQ / AWQ / SmoothQuant 三篇论文 |
| 11 | [解码策略（Greedy / Beam / Sampling）](./notes/11_解码策略.md) | 补充 Top-p 原始论文 + 场景使用建议表 |
| 12 | [推理加速（vLLM / PagedAttention）](./notes/12_推理加速.md) | 补充 Flash Attention / 投机采样 4 篇论文 |

### 🏗️ 工程篇

| 编号 | 主题 | 最近更新 |
|------|------|----------|
| 13 | [MoE 混合专家模型](./notes/13_MoE.md) | 补充 Mixtral / Switch Transformer 论文 |
| 14 | [RAG 检索增强生成](./notes/14_RAG.md) | 添加 IBM RAG 视频 + Self-RAG 论文 |
| 15 | [Agent 与工具调用](./notes/15_Agent.md) | 补充 ReAct / Toolformer 原始论文 |

---

## 🤝 欢迎一起完善

学一个人的笔记，不如一群人共同维护一份高质量知识库。

你可以贡献：
- 📝 **完善某个知识点**的讲解（更清晰的例子、更准确的描述）
- 🎬 **推荐优质视频**（B 站 / YouTube 都欢迎）
- 📄 **补充新的论文**（最新进展、重要综述）
- 🌟 **新增知识点**（Flash Attention 3、DeepSeek 架构……）

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
| 🗂️ 重构目录结构，笔记统一移至 notes/ 文件夹 |

---

<div align="center">

**⭐ Star 一下，下次面试前不慌 ⭐**

*一个人走得快，一群人走得远。欢迎 PR 共建！*

</div>
