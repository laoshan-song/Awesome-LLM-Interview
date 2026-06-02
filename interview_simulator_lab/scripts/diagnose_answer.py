from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from interview_lab import diagnose_answer


def main() -> None:
    parser = argparse.ArgumentParser(description="Diagnose an LLM interview answer.")
    parser.add_argument("--topic", required=True, help="Topic key, e.g. rag/lora/kv_cache/sft/agent.")
    parser.add_argument("--answer", required=True, help="Candidate answer text.")
    args = parser.parse_args()

    print(diagnose_answer(args.topic, args.answer).to_markdown())


if __name__ == "__main__":
    main()

