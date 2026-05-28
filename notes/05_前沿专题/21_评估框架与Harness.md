# LLM 评估框架（lm-evaluation-harness / Lighteval / OpenCompass）

## 面试高频考点
- lm-evaluation-harness 是什么？如何在自己的模型上跑评测？
- Open LLM Leaderboard v2 相比 v1 换了哪些 benchmark？为什么要换？
- Lighteval 和 lm-evaluation-harness 的区别是什么？
- OpenCompass 有什么特点？为什么在国内被广泛使用？
- 什么是 Benchmark 污染？如何通过动态评测缓解？

---

## 一、lm-evaluation-harness

**lm-evaluation-harness** 是 EleutherAI 开发的开源大模型统一评测框架，支持 200+ 评测任务，是 HuggingFace Open LLM Leaderboard 的官方评测后端。

**GitHub**：[github.com/EleutherAI/lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)

### 核心架构

```
lm-evaluation-harness
├── lm_eval/
│   ├── models/          # 模型适配器（HF、OpenAI、vLLM等）
│   ├── tasks/           # 评测任务（YAML配置）
│   └── evaluator.py     # 核心评测逻辑
└── tasks/
    ├── mmlu/
    ├── gsm8k/
    └── ...              # 每个任务一个YAML
```

### 快速上手

```bash
# 安装
pip install lm-eval

# 评测 HuggingFace 模型
lm_eval --model hf \
  --model_args pretrained=Qwen/Qwen3-8B \
  --tasks mmlu,gsm8k,hellaswag \
  --device cuda:0 \
  --batch_size 8 \
  --output_path ./results

# 使用 vLLM 后端加速
lm_eval --model vllm \
  --model_args pretrained=deepseek-ai/DeepSeek-V3,tensor_parallel_size=4 \
  --tasks mmlu_pro,gpqa_diamond \
  --batch_size auto
```

### Python API

```python
import lm_eval

results = lm_eval.simple_evaluate(
    model="hf",
    model_args="pretrained=Qwen/Qwen3-8B",
    tasks=["mmlu", "gsm8k"],
    num_fewshot=5,
    batch_size=8,
)
print(results["results"])
```

### 自定义 Task（YAML 配置）

```yaml
# tasks/my_task/my_task.yaml
task: my_custom_task
dataset_path: my_org/my_dataset
dataset_name: default
output_type: multiple_choice
doc_to_text: "问题：{{question}}\n选项：\nA. {{A}}\nB. {{B}}\nC. {{C}}\nD. {{D}}\n答案："
doc_to_target: "{{answer}}"
metric_list:
  - metric: acc
    aggregation: mean
num_fewshot: 5
```

---

## 二、Open LLM Leaderboard v2 的 6 大新 Benchmark

2024 年 HuggingFace 推出 **Leaderboard v2**，完全替换 v1 的 6 个任务，原因是 v1 任务（HellaSwag、ARC、TruthfulQA 等）已被大量模型接近满分，丧失区分度。

| Benchmark | 领域 | 格式 | 难度 | 目的 |
|-----------|------|------|------|------|
| **MMLU-Pro** | 多学科知识 | 10选1 | ★★★★☆ | MMLU 升级版，减少猜测概率 |
| **GPQA Diamond** | 研究生级科学 | 4选1 | ★★★★★ | 博士级题目，人类专家才能解答 |
| **IFEval** | 指令遵循 | 开放生成 | ★★★☆☆ | 验证模型是否严格遵循格式/长度等约束 |
| **MuSR** | 多步推理 | 开放生成 | ★★★★☆ | 谋杀推理/逻辑谜题等长链推理 |
| **BBH（BIG-Bench Hard）** | 综合推理 | 多种 | ★★★★☆ | BIG-Bench 中最难的 23 个任务 |
| **MATH-lvl-5** | 竞赛数学 | 开放生成 | ★★★★★ | MATH 数据集最难级别题目 |

**关键变化**：v2 更注重**推理能力**（而非知识记忆），更难被针对性优化，区分度更高。

---

## 三、Lighteval（HuggingFace 出品）

**Lighteval** 是 HuggingFace 自研的评测框架，作为 lm-evaluation-harness 的补充和替代：

| 维度 | lm-evaluation-harness | Lighteval |
|------|----------------------|-----------|
| 维护方 | EleutherAI | HuggingFace |
| 任务数量 | 200+ | 持续增长 |
| 与 HF 生态集成 | 好 | **原生集成**（datasets/hub直读）|
| Pipeline 并行评测 | 有限 | 原生支持 |
| 任务定义方式 | YAML | Python 类 + YAML |
| 推荐场景 | 通用评测 | HF 内部模型/快速迭代实验 |

---

## 四、OpenCompass（上海 AI 实验室）

**OpenCompass** 是上海人工智能实验室主导的开源评测框架，在中文评测领域是事实标准。

**GitHub**：[github.com/open-compass/opencompass](https://github.com/open-compass/opencompass)

### 核心特点

- **中文 benchmark 最全**：C-Eval、CMMLU、GaoKao、NaturalBench 等中文专项任务
- **多模态评测**：MMBench、MMStar 等 VLM 评测原生支持
- **API 模型评测**：GPT-4o、Claude、Gemini 等闭源模型一键评测
- **CompassHub**：在线 benchmark 社区，防污染动态更新

```bash
# 快速评测
pip install opencompass
opencompass --models hf_qwen3_8b --datasets ceval_gen mmlu_ppl
```

### 与 lm-evaluation-harness 对比

| 维度 | lm-evaluation-harness | OpenCompass |
|------|----------------------|-------------|
| 中文 benchmark | 较少 | **最全** |
| 英文 benchmark | **最全** | 完整但略少 |
| 多模态 | 支持但弱 | **原生强支持** |
| 国内使用 | 较少 | **主流** |
| 国际使用 | **主流** | 较少 |

---

## 五、Benchmark 污染与动态评测

### 污染的三种形式

| 污染类型 | 描述 | 检测难度 |
|---------|------|---------|
| **直接污染** | 训练数据中包含原始测试题和答案 | 低（n-gram 可检测）|
| **间接污染** | 训练数据包含与测试题高度相似的内容 | 中 |
| **隐性污染** | 爬虫从评测相关网页/讨论中获取了题目 | 高 |

### 污染检测方法

```python
# Min-K% Probability 检测法
# 如果模型对某文本的最低K%的token概率异常高，说明可能见过该文本

def min_k_prob(model, text, k=0.2):
    token_probs = get_token_probs(model, text)
    k_count = max(1, int(len(token_probs) * k))
    min_k_probs = sorted(token_probs)[:k_count]
    return sum(min_k_probs) / k_count  # 分数越高越可能被污染
```

### 动态评测方案

| 方案 | 代表 | 核心思路 |
|------|------|---------|
| **动态更新** | LiveBench | 每月用最新新闻/论文出题，题目持续更新 |
| **人类投票** | Chatbot Arena | 真实用户 A/B 测试，无固定题库 |
| **私有测试集** | 各公司内部 | 不公开，模型无法训练到 |
| **程序验证** | LiveCodeBench | 用最新 LeetCode 周赛题，自动判题 |

---

## 面试延伸

**Q：为什么 GPQA Diamond 被认为是目前最难的 LLM benchmark 之一？**
> GPQA（Graduate-Level Google-Proof Q&A）的题目由博士生/博士后出题，设计要求即使 Google 搜索也无法直接找到答案（Google-Proof），必须真正理解专业知识才能解答。Diamond 子集是其中最难的 198 道题，GPT-4 在此 benchmark 上准确率约 40%，与领域专业人员的 70% 相比仍有差距。

**Q：lm-evaluation-harness 支持 few-shot 评测，few-shot 数量对结果有多大影响？**
> 影响显著。以 MMLU 为例，0-shot 和 5-shot 结果可能相差 5-10 个百分点。原因是少样本示例帮助模型理解任务格式（尤其是选项字母 A/B/C/D 的输出格式），而不是提供知识。因此比较模型性能时，必须确保 few-shot 设置一致，Leaderboard v2 也统一规定了各 benchmark 的 shot 数。

**Q：如何在企业内部建立一套防污染的评测体系？**
> 三层防御：① 使用动态 benchmark（LiveBench/LiveCodeBench）减少静态题库依赖；② 维护私有内部测试集，严格限制访问权限，定期轮换题目；③ 结合 Min-K% Prob 等方法定期扫描训练数据是否包含测试集内容。最重要的是将线上真实用户指标（如 thumbs down rate、任务完成率）作为最终 north star metric。

---

## 原始论文与资源

| 资源 | 链接 |
|------|------|
| lm-evaluation-harness GitHub | [github.com/EleutherAI/lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) |
| Open LLM Leaderboard v2 | [huggingface.co/spaces/open-llm-leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard) |
| Lighteval GitHub | [github.com/huggingface/lighteval](https://github.com/huggingface/lighteval) |
| OpenCompass GitHub | [github.com/open-compass/opencompass](https://github.com/open-compass/opencompass) |
| GPQA 论文 (Rein et al., 2023) | [arxiv.org/abs/2311.12022](https://arxiv.org/abs/2311.12022) |
| Min-K% Prob 污染检测 (Shi et al., 2023) | [arxiv.org/abs/2310.16789](https://arxiv.org/abs/2310.16789) |
| LiveBench (White et al., 2024) | [arxiv.org/abs/2406.19314](https://arxiv.org/abs/2406.19314) |

## 延伸阅读与视频

> 欢迎 PR 补充优质资源
