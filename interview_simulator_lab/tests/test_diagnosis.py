from interview_lab import diagnose_answer


def test_rag_answer_gets_engineering_suggestions() -> None:
    result = diagnose_answer("rag", "RAG 是检索知识库后放进上下文回答，可以降低幻觉，但要关注召回、切块、延迟和评估。")

    assert result.score >= 60
    assert "检索" in result.matched_keywords
    assert result.follow_up


def test_lora_misconception_is_flagged() -> None:
    result = diagnose_answer("lora", "LoRA 是一种量化方法，可以把模型变小。")

    assert result.score < 70
    assert any("LoRA" in suggestion for suggestion in result.suggestions)

