from __future__ import annotations

from dataclasses import dataclass


TOPIC_KEYWORDS: dict[str, set[str]] = {
    "rag": {"检索", "召回", "切块", "重排", "上下文", "引用", "幻觉", "评估", "延迟", "成本"},
    "lora": {"低秩", "冻结", "adapter", "rank", "alpha", "矩阵", "参数", "梯度", "优化器", "merge"},
    "kv_cache": {"自回归", "key", "value", "attention", "缓存", "显存", "序列", "batch", "上下文", "复用"},
    "sft": {"指令", "格式", "质量", "清洗", "去重", "验证集", "覆盖", "风格", "难例", "评估"},
    "agent": {"工具", "ReAct", "action", "observation", "权限", "循环", "日志", "schema", "延迟", "注入"},
}

DIMENSION_KEYWORDS: dict[str, set[str]] = {
    "概念准确性": {"为什么", "原理", "核心", "区别", "不是", "误解"},
    "工程细节": {"线上", "延迟", "成本", "显存", "日志", "评估", "验证集", "schema"},
    "权衡分析": {"代价", "风险", "不能", "失败", "瓶颈", "取舍", "降级"},
    "表达完整度": {"首先", "其次", "最后", "包括", "可以", "需要"},
}


@dataclass(frozen=True)
class Diagnosis:
    topic: str
    score: int
    level: str
    matched_keywords: list[str]
    missing_keywords: list[str]
    strengths: list[str]
    suggestions: list[str]
    follow_up: str

    def to_markdown(self) -> str:
        strengths = "\n".join(f"- {item}" for item in self.strengths)
        suggestions = "\n".join(f"- {item}" for item in self.suggestions)
        matched = "、".join(self.matched_keywords) or "暂无"
        missing = "、".join(self.missing_keywords[:8]) or "暂无"
        return (
            f"## 诊断结果\n\n"
            f"- 主题：{self.topic}\n"
            f"- 得分：{self.score}/100（{self.level}）\n"
            f"- 命中关键词：{matched}\n"
            f"- 建议补充：{missing}\n\n"
            f"### 优点\n{strengths}\n\n"
            f"### 改进建议\n{suggestions}\n\n"
            f"### 追问\n{self.follow_up}\n"
        )


def diagnose_answer(topic: str, answer: str) -> Diagnosis:
    normalized_topic = topic.lower().strip()
    keywords = TOPIC_KEYWORDS.get(normalized_topic, set())
    matched = sorted(keyword for keyword in keywords if keyword.lower() in answer.lower())
    missing = sorted(keywords - set(matched))

    coverage_score = int(60 * len(matched) / max(len(keywords), 1))
    length_score = min(len(answer.strip()) // 6, 20)
    dimension_score = _dimension_score(answer)
    score = min(100, coverage_score + length_score + dimension_score)

    strengths = _build_strengths(matched, answer)
    suggestions = _build_suggestions(normalized_topic, missing, answer)

    return Diagnosis(
        topic=normalized_topic,
        score=score,
        level=_score_level(score),
        matched_keywords=matched,
        missing_keywords=missing,
        strengths=strengths,
        suggestions=suggestions,
        follow_up=_follow_up(normalized_topic, missing),
    )


def _dimension_score(answer: str) -> int:
    score = 0
    for keywords in DIMENSION_KEYWORDS.values():
        if any(keyword.lower() in answer.lower() for keyword in keywords):
            score += 5
    return score


def _score_level(score: int) -> str:
    if score >= 85:
        return "优秀"
    if score >= 70:
        return "合格"
    if score >= 50:
        return "需要补工程细节"
    return "需要重构回答"


def _build_strengths(matched: list[str], answer: str) -> list[str]:
    strengths: list[str] = []
    if matched:
        strengths.append(f"已经覆盖 {len(matched)} 个主题关键词，说明回答抓住了部分核心概念。")
    if len(answer) >= 120:
        strengths.append("回答长度足够支撑展开，适合继续补充结构和例子。")
    if any(word in answer for word in ("线上", "评估", "成本", "延迟", "显存")):
        strengths.append("已经开始从工程落地角度回答，而不只是背概念。")
    return strengths or ["回答给出了初步方向，可以作为后续补全的草稿。"]


def _build_suggestions(topic: str, missing: list[str], answer: str) -> list[str]:
    suggestions = []
    if missing:
        suggestions.append(f"补充这些关键词对应的内容：{'、'.join(missing[:6])}。")
    if "不能" not in answer and "风险" not in answer and "代价" not in answer:
        suggestions.append("增加局限性或失败场景，面试官通常会追问边界条件。")
    if not any(word in answer for word in ("指标", "评估", "验证", "日志")):
        suggestions.append("补一个可量化评估方式，让回答更像工程实践。")
    topic_tip = {
        "rag": "RAG 回答建议按 retrieval、rerank、generation、evaluation 四段组织。",
        "lora": "LoRA 回答建议区分参数高效微调和量化，避免把 LoRA 说成压缩算法。",
        "kv_cache": "KV Cache 回答建议明确缓存的是每层 K/V，不是最终输出文本。",
        "sft": "SFT 回答建议强调数据质量、格式遵循和 held-out 评估。",
        "agent": "Agent 回答建议覆盖工具权限、停止条件和 prompt injection 防护。",
    }
    if topic in topic_tip:
        suggestions.append(topic_tip[topic])
    return suggestions


def _follow_up(topic: str, missing: list[str]) -> str:
    if topic == "rag":
        return "如果检索召回了错误文档，你会如何定位是 query rewrite、embedding、chunking 还是 rerank 的问题？"
    if topic == "lora":
        return "如果 LoRA 微调后训练集效果好但真实面试问题泛化差，你会怎么排查数据和 rank 设置？"
    if topic == "kv_cache":
        return "当 batch size 和上下文长度同时升高时，KV Cache 显存怎么估算？"
    if topic == "sft":
        return "如果 SFT 后模型学会了固定模板但答案事实性下降，你会如何调整数据？"
    if topic == "agent":
        return "如何防止 Agent 把网页里的恶意提示当成系统指令执行？"
    if missing:
        return f"你刚才没有提到 {missing[0]}，它在这个问题里为什么重要？"
    return "你能举一个真实工程场景说明这个知识点怎么落地吗？"

