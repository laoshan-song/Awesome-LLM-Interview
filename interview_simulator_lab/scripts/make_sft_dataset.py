from __future__ import annotations

import argparse
import json
from pathlib import Path


SYSTEM_PROMPT = "你是一个严格但有帮助的 LLM 面试官，负责诊断候选人的回答并给出追问。"


def to_sft_record(row: dict) -> dict:
    user = (
        f"面试主题：{row['topic']}\n"
        f"面试问题：{row['question']}\n"
        f"候选人回答：{row['weak_answer']}\n\n"
        "请从概念准确性、工程细节、权衡分析、表达完整度四个维度诊断，并给出一个追问。"
    )
    assistant = (
        f"诊断：{row['diagnosis']}\n"
        f"参考答案：{row['good_answer']}\n"
        f"追问：{row['follow_up']}"
    )
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ]
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build SFT JSONL from seed interview data.")
    parser.add_argument(
        "--input",
        default="data/seed_interviews.jsonl",
        help="Input JSONL. Can be a comma-separated list, e.g. data/seed_interviews.jsonl,data/notes_interviews.jsonl.",
    )
    parser.add_argument("--output", default="data/sft_interview_diagnosis.jsonl")
    args = parser.parse_args()

    input_paths = [Path(item.strip()) for item in args.input.split(",") if item.strip()]
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    with output_path.open("w", encoding="utf-8") as target:
        for input_path in input_paths:
            with input_path.open("r", encoding="utf-8") as source:
                for line in source:
                    if line.strip():
                        target.write(json.dumps(to_sft_record(json.loads(line)), ensure_ascii=False) + "\n")
                        count += 1

    print(f"Wrote {count} records to {output_path}")


if __name__ == "__main__":
    main()
