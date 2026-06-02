from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from interview_lab import diagnose_answer


def load_cases(path: Path) -> list[dict]:
    cases = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                cases.append(json.loads(line))
    return cases


def evaluate_case(case: dict) -> dict:
    result = diagnose_answer(case["topic"], case["answer"])
    matched = set(result.matched_keywords)
    required = set(case.get("must_match", []))
    missing_required = sorted(required - matched)
    passed = result.score >= case["min_score"] and not missing_required
    return {
        "topic": case["topic"],
        "score": result.score,
        "min_score": case["min_score"],
        "missing_required": missing_required,
        "passed": passed,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate diagnosis rules on curated cases.")
    parser.add_argument("--cases", default="data/eval_cases.jsonl")
    args = parser.parse_args()

    reports = [evaluate_case(case) for case in load_cases(Path(args.cases))]
    passed = sum(1 for report in reports if report["passed"])
    total = len(reports)

    for report in reports:
        status = "PASS" if report["passed"] else "FAIL"
        missing = "、".join(report["missing_required"]) or "-"
        print(
            f"{status} topic={report['topic']} "
            f"score={report['score']}/{report['min_score']} missing_required={missing}"
        )

    print(f"summary: {passed}/{total} passed")
    if passed != total:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
