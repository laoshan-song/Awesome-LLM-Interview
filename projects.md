# 🛠️ LLM 项目库

这份列表只收录两类东西：

1. 学完知识点后能直接动手的 GitHub 项目
2. 能支撑你做实验、评测、微调的 Kaggle 数据集或比赛

默认筛选标准：

- 能较快跑起来
- 能明确对应到仓库里的某块知识点
- 能改出自己的版本，适合写进简历或面试项目经历

---

## 1. RAG 项目

### 入门

| 项目 | 类型 | 链接 | 适合先学哪些内容 | 练到什么 |
|------|------|------|------------------|----------|
| RAG from Scratch | GitHub | [pguso/rag-from-scratch](https://github.com/pguso/rag-from-scratch) | RAG / Prompt / 基础向量检索 | 手搓最小 RAG 闭环 |
| Sample RAG Knowledge Item Dataset | Kaggle | [sample-rag-knowledge-item-dataset](https://www.kaggle.com/datasets/dkhundley/sample-rag-knowledge-item-dataset) | RAG / chunking / retrieval | 试不同切块、召回和 prompt 策略 |

### 进阶

| 项目 | 类型 | 链接 | 适合先学哪些内容 | 练到什么 |
|------|------|------|------------------|----------|
| rag-chatbot | GitHub | [mrankitvish/rag-chatbot](https://github.com/mrankitvish/rag-chatbot) | RAG / LangChain / PGVector | FastAPI + 向量库 + 本地模型服务 |
| fullstack-chatbot-with-langchain-and-rag | GitHub | [logreg-n-coffee/fullstack-chatbot-with-langchain-and-rag](https://github.com/logreg-n-coffee/fullstack-chatbot-with-langchain-and-rag) | RAG / 前后端联调 / Prompt | 做成可演示 Web 产品 |
| agentic_rag_project | GitHub | [serkanyasr/agentic_rag_project](https://github.com/serkanyasr/agentic_rag_project) | Agentic RAG / FastAPI / pgvector | 多阶段检索、模块化 RAG 服务 |

### 评测与优化

| 项目 | 类型 | 链接 | 适合先学哪些内容 | 练到什么 |
|------|------|------|------------------|----------|
| RAG-Based Hallucination Reduction in LLMs | Kaggle | [rag-based-hallucination-reduction-in-llms](https://www.kaggle.com/datasets/algozee/rag-based-hallucination-reduction-in-llms) | 幻觉 / RAG / 评估 | 比较有无 RAG 的事实性差异 |
| RAG QA Logs & Corpus Data | Kaggle | [rag-qa-evaluation-logs-and-corpus](https://www.kaggle.com/datasets/tarekmasryo/rag-qa-evaluation-logs-and-corpus) | RAGAS / retrieval telemetry / 评估 | 做 retrieval quality、hallucination risk、成本分析 |
| rag-langchain-ragas | GitHub | [benitomartin/rag-langchain-ragas](https://github.com/benitomartin/rag-langchain-ragas) | RAGAS / LangChain / 评测 | 练 RAG 评测 pipeline |

---

## 2. 微调与对齐项目

### 入门

| 项目 | 类型 | 链接 | 适合先学哪些内容 | 练到什么 |
|------|------|------|------------------|----------|
| QLoRA | GitHub | [artidoro/qlora](https://github.com/artidoro/qlora) | LoRA / QLoRA / 量化 | 跑通 4-bit 微调与 adapter 训练 |
| Fine-tune-a-LLM | GitHub | [medss19/Fine-tune-a-LLM](https://github.com/medss19/Fine-tune-a-LLM) | SFT / QLoRA / 指令数据 | 做一个完整 domain SFT 示例 |

### 数据与比赛

| 项目 | 类型 | 链接 | 适合先学哪些内容 | 练到什么 |
|------|------|------|------------------|----------|
| LLM Classification Finetuning | Kaggle 比赛 | [competition link](https://www.kaggle.com/competitions/llm-classification-finetuning/overview/description/abstract/abstract) | SFT / 分类微调 / 评估 | 练验证集设计、提交和误差分析 |
| 100K + Medium Articles Dataset For LLM FineTuning | Kaggle 数据集 | [dataset link](https://www.kaggle.com/datasets/meruvulikith/193k-medium-articles-dataset-for-llm-finetuning) | continued pretraining / summarization | 自建领域微调数据管线 |
| nemotron-math-v2-sft-hard-tools | Kaggle 数据集 | [dataset link](https://www.kaggle.com/datasets/ritwikakancharla/nemotron-math-v2-sft-hard-tools) | reasoning SFT / tool use | 做带工具调用的推理微调实验 |

### 对齐框架

| 项目 | 类型 | 链接 | 适合先学哪些内容 | 练到什么 |
|------|------|------|------------------|----------|
| OpenRLHF | GitHub | [OpenRLHF/OpenRLHF](https://github.com/OpenRLHF/OpenRLHF) | RLHF / PPO / DPO | 理解对齐训练脚手架 |
| veRL | GitHub | [verl-project/verl](https://github.com/verl-project/verl) | RLVR / post-training | 看现代后训练工程做法 |
| TRL | GitHub | [huggingface/trl](https://github.com/huggingface/trl) | SFT / DPO / PPO | 用最常见工具链跑对齐实验 |

---

## 3. 推理与部署项目

### 推理服务

| 项目 | 类型 | 链接 | 适合先学哪些内容 | 练到什么 |
|------|------|------|------------------|----------|
| vLLM | GitHub | [vllm-project/vllm](https://github.com/vllm-project/vllm) | vLLM / PagedAttention / serving | OpenAI-compatible 高吞吐推理服务 |
| SGLang | GitHub | [sgl-project/sglang](https://github.com/sgl-project/sglang) | RadixAttention / 推理框架 | 多轮对话、公用前缀复用 |
| llama.cpp | GitHub | [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | GGUF / 量化 / 本地推理 | CPU/边缘端部署与量化实践 |
| vllama | GitHub | [erkkimon/vllama](https://github.com/erkkimon/vllama) | OpenAI API / 本地部署 | 组合 Ollama 与 vLLM 风格服务 |

### 练手机会

| 项目 | 类型 | 链接 | 适合先学哪些内容 | 练到什么 |
|------|------|------|------------------|----------|
| vllm-mlx | GitHub | [waybarrios/vllm-mlx](https://github.com/waybarrios/vllm-mlx) | OpenAI server / batching / multimodal serving | 看一个兼容 API 的完整推理服务实现 |
| agentnovax-api-rag-springboot-ollama-pgvector | GitHub | [agentnovax-api-rag-springboot-ollama-pgvector](https://github.com/agentnovax/agentnovax-api-rag-springboot-ollama-pgvector) | RAG / Java 后端 / PGVector | 如果你想走 Java AI 工程方向，这个更贴近业务服务 |

---

## 4. Agent 项目

### 入门

| 项目 | 类型 | 链接 | 适合先学哪些内容 | 练到什么 |
|------|------|------|------------------|----------|
| langgraph-101 | GitHub | [langchain-ai/langgraph-101](https://github.com/langchain-ai/langgraph-101) | LangGraph / stateful workflow | 先把基本图结构跑通 |
| LangGraph | GitHub | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | Agent / graph orchestration | 官方框架本体与 examples |

### 工程化

| 项目 | 类型 | 链接 | 适合先学哪些内容 | 练到什么 |
|------|------|------|------------------|----------|
| Deb8flow | GitHub | [iason-solomos/Deb8flow](https://github.com/iason-solomos/Deb8flow) | multi-agent / debate / evaluation | 多 Agent 仲裁与工作流编排 |
| Multi-Agent-Orchestrator | GitHub | [OmishaPatel/Multi-Agent-Orchestrator](https://github.com/OmishaPatel/Multi-Agent-Orchestrator) | Agent / orchestration / backend | 任务拆解、服务化、模块边界 |
| todo-work-agent | GitHub | [boemer00/todo-work-agent](https://github.com/boemer00/todo-work-agent) | LangGraph / 工具调用 / 产品化 | 做一个接近真实业务的 portfolio 项目 |

### 评测与基准

| 项目 | 类型 | 链接 | 适合先学哪些内容 | 练到什么 |
|------|------|------|------------------|----------|
| GTA | GitHub | [open-compass/GTA](https://github.com/open-compass/GTA) | tool agent benchmark / evaluation | 评估 agent 工具使用能力 |

---

## 5. 多模态项目

### 入门

| 项目 | 类型 | 链接 | 适合先学哪些内容 | 练到什么 |
|------|------|------|------------------|----------|
| LLaVA | GitHub | [haotian-liu/LLaVA](https://github.com/haotian-liu/LLaVA) | VLM / projector / instruction tuning | 理解经典图文模型结构 |
| InternVL | GitHub | [OpenGVLab/InternVL](https://github.com/OpenGVLab/InternVL) | dynamic resolution / OCR / VLM | 看高分辨率视觉路线 |

### 进阶

| 项目 | 类型 | 链接 | 适合先学哪些内容 | 练到什么 |
|------|------|------|------------------|----------|
| SlowFast-LLaVA | GitHub | [apple/ml-slowfast-llava](https://github.com/apple/ml-slowfast-llava) | video LLM / VLM inference | 从图像多模态走到视频理解 |
| MG-LLaVA | GitHub | [PhoenixZ810/MG-LLaVA](https://github.com/PhoenixZ810/MG-LLaVA) | multimodal instruction tuning | 看更细粒度的视觉指令调优 |

### 数据集

| 项目 | 类型 | 链接 | 适合做什么 |
|------|------|------|------------|
| Response Score Dataset on VLM | Kaggle 数据集 | [dataset link](https://www.kaggle.com/datasets/tangx0121/vlm-response-score-dataset) | 做 VLM router / judge / response quality 评测 |
| Surveillance VLM: Weapon & Knife Detection Dataset | Kaggle 数据集 | [dataset link](https://www.kaggle.com/datasets/simuletic/surveillance-vlm-weapon-and-knife-detection-dataset) | 做场景化 VLM instruction tuning 或安全检测 demo |

---

## 6. 评估项目

| 项目 | 类型 | 链接 | 适合先学哪些内容 | 练到什么 |
|------|------|------|------------------|----------|
| lm-evaluation-harness | GitHub | [EleutherAI/lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) | benchmark / model eval | 跑通标准 LLM benchmark |
| OpenCompass | GitHub | [open-compass/opencompass](https://github.com/open-compass/opencompass) | 中文评测 / vLLM backend / benchmark | 做中文模型评测报告 |
| RAGAS | GitHub | [vibrantlabs-ai/ragas](https://github.com/vibrantlabs-ai/ragas) | RAG eval / LLM-as-judge | 给 RAG 系统加自动评测 |

---

## 7. 推荐路线

### 路线 A：最快做出一个能演示的项目

1. `RAG from Scratch`
2. `rag-chatbot`
3. `rag-langchain-ragas`

### 路线 B：训练和推理都要碰一遍

1. `QLoRA`
2. `Fine-tune-a-LLM`
3. `vLLM` 或 `llama.cpp`

### 路线 C：目标是 Agent 工程岗

1. `langgraph-101`
2. `Deb8flow`
3. `todo-work-agent`

---

## 8. 简历怎么写

如果你真做完一个项目，最好至少补这 4 样东西：

1. 数据来源和清洗方式
2. 模型/框架选型理由
3. 指标或 benchmark 结果
4. 你自己做过的改动，而不是“跑通官方 demo”
