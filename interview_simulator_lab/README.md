# LLM 面试模拟与回答诊断实验室

这个子项目把面试准备日志升级成一个可演示的工程闭环：从面试问答数据构造开始，做回答质量诊断、模拟追问，再扩展到小模型 SFT/LoRA 微调。

## 项目目标

- 把零散 LLM 笔记转成可训练的 instruction 数据。
- 对候选人的回答做结构化诊断：概念准确性、工程细节、权衡分析、表达完整度。
- 用 CLI 模拟面试官追问，形成可复盘的练习记录。
- 提供 QLoRA 微调脚本模板，用小模型学习“面试官风格”和“诊断反馈格式”。

## 目录结构

```text
interview_simulator_lab/
  data/
    seed_interviews.jsonl        # 种子面试问答数据
  scripts/
    diagnose_answer.py           # 本地回答诊断 CLI
    make_sft_dataset.py          # 生成 SFT 训练数据
    qlora_sft.py                 # 可选：LoRA/QLoRA 微调脚本
    tiny_markov_baseline.py      # 无深度学习依赖的 toy LM 基线
  src/interview_lab/
    diagnosis.py                 # 诊断规则与评分
    prompt_bank.py               # 面试题库
    simulator.py                 # 模拟面试流程
  tests/
    test_diagnosis.py
```

## 快速运行

只跑诊断，不需要安装大模型依赖：

```bash
cd interview_simulator_lab
python scripts/diagnose_answer.py --topic rag --answer "RAG 是先检索知识库，再把相关片段放进 prompt，让模型基于上下文回答，可以降低幻觉。线上要关注召回率、切块、重排、引用和延迟。"
```

生成 SFT 数据：

```bash
python scripts/make_sft_dataset.py --output data/sft_interview_diagnosis.jsonl
```

从仓库 `notes/` 自动扩充训练样本：

```bash
python scripts/build_notes_interviews.py --notes-root ../notes --output data/notes_interviews.jsonl
python scripts/make_sft_dataset.py --input data/seed_interviews.jsonl,data/notes_interviews.jsonl --output data/sft_interview_diagnosis.jsonl
```

运行 toy LM 基线：

```bash
python scripts/tiny_markov_baseline.py --data data/seed_interviews.jsonl --prompt "请追问 RAG 的线上评估指标"
```

基础自检：

```bash
python scripts/smoke_test.py
```

运行规则评估：

```bash
python scripts/evaluate_diagnosis.py --cases data/eval_cases.jsonl
```

这个 toy baseline 不是为了性能，而是用来展示“从数据到可生成模型”的最小训练闭环。真正用于简历项目时，应使用 `qlora_sft.py` 对 `Qwen2.5-0.5B-Instruct`、`Qwen2.5-1.5B-Instruct` 或同级别小模型做 LoRA 微调。

### 训练一个模拟面试 LLM

推荐先训练“诊断与追问风格”，不要指望 0.5B 小模型记住所有知识。知识本身继续来自 `notes/` 或 RAG，上层模型学习的是：发现回答漏洞、按维度反馈、给出追问。

```bash
pip install -e ".[train]"
python scripts/build_notes_interviews.py --notes-root ../notes --output data/notes_interviews.jsonl
python scripts/make_sft_dataset.py --input data/seed_interviews.jsonl,data/notes_interviews.jsonl --output data/sft_interview_diagnosis.jsonl
python scripts/qlora_sft.py \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --data data/sft_interview_diagnosis.jsonl \
  --output outputs/interview-diagnosis-lora \
  --max-steps 200
```

Linux + NVIDIA GPU 环境可以加 `--load-in-4bit` 做 QLoRA；Windows 本地更建议先不用 4-bit，或在 WSL2 / 云 GPU 上跑。训练完成后，用固定评估集检查格式遵循率、诊断点覆盖率、追问相关性，再决定是否扩大数据。

## 微调路线

1. 数据构造：从笔记中抽取 `question / good_answer / weak_answer / diagnosis / follow_up`。
2. SFT 格式：把输入整理成“候选人回答 -> 面试官诊断”的 instruction 数据。
3. 训练方法：使用 PEFT LoRA，先训输出格式和诊断维度，不追求让小模型记住全部知识。
4. 评估指标：格式遵循率、诊断点覆盖率、追问相关性、是否指出明显错误。
5. 产品化：把诊断 CLI 扩展成 Web 或 API，接入你的 LLM 笔记作为 RAG 上下文。

## 当前评估集

`data/eval_cases.jsonl` 维护了一组人工标注样本，每条样本包含：

- `topic`：面试主题。
- `answer`：候选人回答。
- `min_score`：期望最低诊断分。
- `must_match`：诊断器必须识别出的关键点。

这个评估集目前规模很小，作用是防止后续改规则时把明显正确的回答误判。后续可以继续扩展负样本，例如“把 LoRA 误认为量化”“把 KV Cache 误认为结果缓存”等。

## 简历表述

可以写成：

> 构建 LLM 面试模拟与回答诊断系统，基于自建问答数据生成 SFT 样本，使用 LoRA 微调小参数模型学习结构化面试反馈格式；设计概念准确性、工程细节、权衡分析、表达完整度等诊断维度，并实现本地 CLI 评测与追问生成闭环。
