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

每篇笔记包含：**面试高频考点 + 核心原理 + 外部图解 + 原始论文 + 视频讲解 + 工程落地追问**。

### 🔥 推荐优先看这几篇

- [LLM 从输入到输出](./notes/00_LLM总览/01_LLM从输入到输出.md)：用一条链路讲清 token、embedding、Transformer、logits、解码
- [LLM 能力来源与 Scaling Law](./notes/00_LLM总览/02_LLM能力来源与Scaling_Law.md)：解释能力从数据、参数、计算和对齐中怎么来，补 Scaling Law 论文图
- [从训练到部署：LLM 生命周期](./notes/00_LLM总览/03_训练到部署全流程.md)：串起数据、预训练、后训练、评估、部署和反馈闭环
- [Embedding 与向量检索](./notes/06_工程实践/03_Embedding与向量检索.md)：讲清语义检索、Hybrid Search、Rerank 和向量库选型
- [模型网关与成本治理](./notes/06_工程实践/05_模型网关与成本治理.md)：把模型路由、缓存、降级、成本监控讲成生产系统能力
- [LLM 安全与红队](./notes/06_工程实践/06_LLM安全与红队.md)：覆盖 Prompt Injection、RAG 权限、Agent 工具安全和审计
- [Transformer 架构详解](./notes/01_基础架构/03_Transformer架构.md)：补了官方论文架构图和快速回答模板
- [LoRA 及参数高效微调（PEFT）](./notes/02_训练与对齐/08_LoRA与PEFT.md)：补了 LoRA 原论文图和工程落地说明
- [RAG 检索增强生成](./notes/05_前沿专题/14_RAG.md)：补了 NVIDIA 官方流程图和更工程化的拆解
- [MoE 混合专家模型](./notes/05_前沿专题/13_MoE.md)：补了官方路由图和 serving 难点说明
- [SFT 有监督微调](./notes/02_训练与对齐/06_SFT.md)：补了 Self-Instruct 论文图和数据验收清单
- [RLHF / DPO / PPO 对比](./notes/02_训练与对齐/07_RLHF_DPO_PPO.md)：补了 InstructGPT/RLHF 三阶段论文图和 PPO 工程角色说明
- [推理加速](./notes/03_推理与优化/12_推理加速.md)：补了 FlashAttention 原论文图和 TTFT/TPOT 诊断维度
- [解码策略](./notes/03_推理与优化/11_解码策略.md)：补了 Nucleus Sampling 论文图和参数联调建议

### ⚡ 面试速记网页

> **[→ 打开速记网页（在线访问）](https://laoshan-song.github.io/Awesome-LLM-Interview/cheatsheet.html)**
>
> 95 道高频考题，15 大模块，支持搜索、标签筛选、一键展开、核心论文路线图、模拟面试问答诊断、薄弱点判断测试、本地账号登录和个人记忆 notes。测试结果会直接跳转到 GitHub 上对应的 notes 文档。面试前 30 分钟速刷专用。

> 如果你觉得有用，点个 ⭐ Star 是对我最大的鼓励！

### 🧪 真实面试题型

> **[→ 打开真实 LLM 面试题型整理](./real_interview_questions.md)**
>
> 按 LLM 基础、训练对齐、推理部署、RAG、Agent、Prompt、安全、评估、系统设计和项目追问整理真实高频问法，并链接到对应 notes。

---

## 📚 知识点目录

### 🧭 零、LLM 总览

| 编号 | 主题 | 最近更新 |
|------|------|----------|
| 00-01 | [LLM 从输入到输出](./notes/00_LLM总览/01_LLM从输入到输出.md) | **新增**：从 tokenization 到 decoding 的完整链路 |
| 00-02 | [LLM 能力来源与 Scaling Law](./notes/00_LLM总览/02_LLM能力来源与Scaling_Law.md) | **新增**：Scaling Law 论文图、参数/数据/计算/对齐与涌现能力 |
| 00-03 | [从训练到部署：LLM 生命周期](./notes/00_LLM总览/03_训练到部署全流程.md) | **新增**：数据、预训练、后训练、评估、部署、监控闭环 |

### 🔤 一、基础架构

| 编号 | 主题 | 最近更新 |
|------|------|----------|
| 01 | [LLM 核心名词解释](./notes/01_基础架构/01_名词解释.md) | 补全 Token / Attention / KV Cache 等 30+ 核心术语 |
| 02 | [分词算法（BPE / WordPiece / SentencePiece）](./notes/01_基础架构/02_分词算法.md) | 添加 Karpathy 视频、官方 tokenizer 工具链和论文链接 |
| 03 | [Transformer 架构详解](./notes/01_基础架构/03_Transformer架构.md) | 添加 3Blue1Brown 可视化视频 + 原版论文 |
| 04 | [位置编码（RoPE / ALiBi / sinusoidal）](./notes/01_基础架构/04_位置编码.md) | 补充 RoPE / ALiBi 论文 + 外推方案对比 |
| 05 | [主流模型架构对比（LLaMA / Qwen / DeepSeek）](./notes/01_基础架构/05_主流模型架构对比.md) | MLA、RMSNorm、SwiGLU 等架构细节 |
| 06 | [国产主流模型全景（DeepSeek / Qwen / GLM / MiniMax）](./notes/01_基础架构/06_国产主流模型全景.md) | **新增**：DeepSeek-V3/R1/V4、Qwen3混合思考、MiniMax Lightning Attention 🔥 |

### ⚙️ 二、训练与对齐

| 编号 | 主题 | 最近更新 |
|------|------|----------|
| 07 | [预训练 vs 微调 vs RLHF](./notes/02_训练与对齐/05_预训练与微调.md) | 补充 InstructGPT / LIMA 论文、三阶段流程和训练工具链 |
| 08 | [SFT 有监督微调](./notes/02_训练与对齐/06_SFT.md) | 补充数据质量分析 + loss 计算细节 |
| 09 | [RLHF / DPO / PPO 对比](./notes/02_训练与对齐/07_RLHF_DPO_PPO.md) | 添加李沐精读视频 + DPO 完整推导 |
| 10 | [LoRA 及参数高效微调（PEFT）](./notes/02_训练与对齐/08_LoRA与PEFT.md) | 添加论文精读视频 + QLoRA 细节 |
| 11 | [预训练数据处理](./notes/02_训练与对齐/09_预训练数据处理.md) | 数据清洗、去重、配比策略、FineWeb/Dolma/Datatrove 链接 |
| 12 | [2025 前沿对齐技术（RLVR / DAPO / RLAIF）](./notes/02_训练与对齐/10_前沿对齐技术.md) | **新增**：DAPO/Dr.GRPO/OpenRLHF/veRL/Constitutional AI 🔥 |

### 🚀 三、推理与优化

| 编号 | 主题 | 最近更新 |
|------|------|----------|
| 13 | [KV Cache 原理与优化](./notes/03_推理与优化/09_KV_Cache.md) | 补充 Prefill/Decode 外部图、显存公式、GQA / PagedAttention |
| 14 | [量化（INT8 / INT4 / GPTQ / AWQ）](./notes/03_推理与优化/10_量化.md) | 补充 AWQ 论文图、GPTQ / AWQ / SmoothQuant 论文和工具链 |
| 15 | [解码策略（Greedy / Beam / Sampling）](./notes/03_推理与优化/11_解码策略.md) | 补充 Top-p 论文 + 场景使用建议 |
| 16 | [推理加速（Flash Attention / vLLM / 投机采样）](./notes/03_推理与优化/12_推理加速.md) | 补充 Flash Attention / 投机采样 4 篇论文 |
| 17 | [推理框架对比（vLLM / SGLang / llama.cpp）](./notes/03_推理与优化/13_推理框架对比.md) | **新增**：RadixAttention、GGUF量化、Disaggregated P/D、选型指南 🔥 |

### 🖥️ 四、分布式训练

| 编号 | 主题 | 最近更新 |
|------|------|----------|
| 18 | [数据并行与模型并行](./notes/04_分布式训练/01_数据并行与模型并行.md) | ZeRO 三阶段、张量/流水线并行对比 |
| 19 | [显存优化技巧](./notes/04_分布式训练/02_显存优化技巧.md) | 梯度检查点、混合精度、显存占用公式 |

### 🔬 五、前沿专题

| 编号 | 主题 | 最近更新 |
|------|------|----------|
| 20 | [MoE 混合专家模型](./notes/05_前沿专题/13_MoE.md) | 补充 Mixtral / Switch Transformer 论文 |
| 21 | [RAG 检索增强生成](./notes/05_前沿专题/14_RAG.md) | 添加 Self-RAG 论文 + LangChain 视频 |
| 22 | [Agent 与工具调用](./notes/05_前沿专题/15_Agent.md) | 补充 ReAct 外部图、Toolformer 论文和工具调用边界 |
| 23 | [Prompt Engineering](./notes/05_前沿专题/16_Prompt_Engineering.md) | CoT / ToT 论文图、Self-Consistency、提示注入防御和课程链接 |
| 24 | [大模型幻觉与评估](./notes/05_前沿专题/17_大模型幻觉与评估.md) | 幻觉分类、MMLU/HumanEval、LLM-as-Judge |
| 25 | [推理时计算扩展（Test-Time Compute）](./notes/05_前沿专题/18_推理时计算扩展.md) | DeepSeek-R1、GRPO、PRM 全面解析 |
| 26 | [多模态大模型（VLM）](./notes/05_前沿专题/19_多模态大模型.md) | GPT-4o/InternVL 架构、视觉编码器对比 |
| 27 | [GraphRAG 与高级 RAG](./notes/05_前沿专题/20_GraphRAG与高级RAG.md) | GraphRAG、HyDE、Self-RAG、RAGAS 评估 |
| 28 | [评估框架与 Harness](./notes/05_前沿专题/21_评估框架与Harness.md) | **新增**：MTEB 评估图、lm-eval-harness、Open LLM Leaderboard v2、OpenCompass 🔥 |
| 29 | [Agent 框架与 MCP 协议](./notes/05_前沿专题/22_Agent框架与MCP.md) | **新增**：LangGraph、AutoGen、OpenAI Agents SDK、MCP/A2A 协议 🔥 |

### 🧱 六、工程实践

| 编号 | 主题 | 最近更新 |
|------|------|----------|
| 30 | [LLM 应用架构与 LLMOps](./notes/06_工程实践/01_LLM应用架构与LLMOps.md) | **新增**：LLMOps 外部图、生产架构、发布回滚、商业项目指标 |
| 31 | [生产 RAG 排障指南](./notes/06_工程实践/02_生产RAG排障指南.md) | **新增**：NVIDIA RAG 图、生产排障 Runbook、评估集构建 |
| 32 | [Embedding 与向量检索](./notes/06_工程实践/03_Embedding与向量检索.md) | **新增**：SBERT 双塔图、Hybrid Search、Rerank、向量库排障 |
| 33 | [上下文工程与长上下文应用](./notes/06_工程实践/04_上下文工程与长上下文应用.md) | **新增**：Lost in the Middle 图、上下文编排、长上下文排障 |
| 34 | [模型网关与成本治理](./notes/06_工程实践/05_模型网关与成本治理.md) | **新增**：模型路由论文、缓存、限流、降级、成本归因 |
| 35 | [LLM 安全与红队](./notes/06_工程实践/06_LLM安全与红队.md) | **新增**：Prompt Injection 论文、RAG 权限、Agent 工具安全、红队工具 |

---

## 🛠️ 学完可做项目

我单独整理了一份 **项目实战库**，按主题拆成 `RAG / 微调 / 推理部署 / Agent / 多模态 / 评估` 六类，每类都有 GitHub 项目和 Kaggle 数据入口。

> **[→ 打开项目库](./projects.md)**

如果你只想先选一个最容易做成作品的方向，建议顺序是：

1. 本地 RAG
2. QLoRA 微调
3. LangGraph 多 Agent

### 🧪 仓库内实战项目

- [商业级 RAG 工单助手](./commercial_rag_ticket_assistant)：企业知识库问答、工单分流、审计与评估指标。
- [LLM 面试模拟与回答诊断实验室](./interview_simulator_lab)：把面试笔记转成 SFT 数据，提供回答诊断 CLI、模拟追问和 QLoRA 微调脚本模板。

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
| 📚 补全核心知识点（基础 / 训练 / 推理 / 工程） |
| 📄 为所有知识点补充原始论文 arxiv 链接 |
| 🎬 添加 Karpathy / 3Blue1Brown / 李沐等优质视频资源 |
| 🗂️ 重构目录：按主题分为 7 大模块，覆盖 LLM 总览、基础架构、训练对齐、推理优化、分布式训练、前沿专题、工程实践 |
| 🚀 新增 2026 前沿专题：TTC/DeepSeek-R1/GRPO、多模态VLM、GraphRAG |
| ⚡ 升级面试速记网页（cheatsheet.html）：95 道高频考题、15 大模块，支持搜索/筛选、核心论文路线图、模拟面试诊断、薄弱点测试、本地账号、个人记忆 notes 和 GitHub notes 跳转 |
| 📄 导入核心原始论文路线图：覆盖 Transformer、Scaling Law、RoPE、GQA、FlashAttention、vLLM、LoRA/QLoRA、RLHF/DPO、CoT、RAG、MTEB、Agent、RAGAS、SWE-bench |
| 🇨🇳 新增国产模型全景：DeepSeek-V3/R1、Qwen3混合思考、GLM-4、MiniMax Lightning Attention |
| 🔧 新增前沿框架：vLLM/SGLang/llama.cpp推理框架对比、DAPO/RLVR对齐技术、lm-eval-harness评估、LangGraph/MCP协议 |
| 🖼️ 补充外部图解和资料链接：全库 24 张外部图、450+ 外部链接，覆盖 Transformer、Scaling Law、Prompt、RAG、KV Cache、Agent、LLMOps、Embedding、量化、评估、长上下文等核心主题 |
| 🧪 新增真实 LLM 面试题型整理：覆盖基础原理、RAG、LoRA/RLHF/DPO、推理部署、Agent、安全、评估、系统设计和项目追问 |

---

<div align="center">

**⭐ Star 一下，下次面试前不慌 ⭐**

*一个人走得快，一群人走得远。欢迎 PR 共建！*

</div>
