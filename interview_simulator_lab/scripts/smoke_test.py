from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from interview_lab import diagnose_answer


def main() -> None:
    rag = diagnose_answer("rag", "RAG 通过检索、召回、切块、重排和上下文引用降低幻觉，也要评估延迟和成本。")
    lora = diagnose_answer("lora", "LoRA 是一种量化方法，可以把模型变小。")

    assert rag.score >= 60, rag
    assert "检索" in rag.matched_keywords, rag
    assert lora.score < 70, lora
    assert lora.suggestions, lora
    print("smoke test passed")


if __name__ == "__main__":
    main()

