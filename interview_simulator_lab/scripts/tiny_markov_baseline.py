from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path


def tokenize(text: str) -> set[str]:
    tokens = set()
    for raw in text.replace("，", " ").replace("。", " ").replace("？", " ").split():
        token = raw.strip().lower()
        if token:
            tokens.add(token)
    for keyword in ("RAG", "LoRA", "QLoRA", "KV", "SFT", "Agent", "评估", "追问", "显存", "召回"):
        if keyword.lower() in text.lower():
            tokens.add(keyword.lower())
    return tokens


def best_seed_record(path: Path, prompt: str) -> dict:
    prompt_tokens = tokenize(prompt)
    best_score = -1
    best_row = None
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            row = json.loads(line)
            row_tokens = tokenize(" ".join([row["topic"], row["question"], row["good_answer"], row["follow_up"]]))
            score = len(prompt_tokens & row_tokens)
            if score > best_score:
                best_score = score
                best_row = row
    if best_row is None:
        raise ValueError("No seed interview records found.")
    return best_row


def train_char_markov(text: str, order: int = 3) -> dict[str, list[str]]:
    model: dict[str, list[str]] = defaultdict(list)
    padded = "~" * order + text
    for index in range(len(padded) - order):
        state = padded[index : index + order]
        model[state].append(padded[index + order])
    return dict(model)


def generate(model: dict[str, list[str]], prompt: str, order: int = 3, max_chars: int = 240) -> str:
    state = (("~" * order) + prompt)[-order:]
    output = []
    states = [key for key in model if key != "~" * order]
    for _ in range(max_chars):
        choices = model.get(state)
        if not choices:
            state = random.choice(states)
            choices = model[state]
        char = random.choice(choices)
        output.append(char)
        state = (state + char)[-order:]
    return "".join(output).strip()


def load_training_text(path: Path) -> str:
    parts = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            row = json.loads(line)
            parts.extend([row["question"], row["good_answer"], row["diagnosis"], row["follow_up"]])
    return "\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a tiny character-level Markov baseline.")
    parser.add_argument("--data", default="data/seed_interviews.jsonl")
    parser.add_argument("--prompt", default="请追问 RAG 的线上评估指标")
    parser.add_argument("--order", type=int, default=3)
    args = parser.parse_args()

    random.seed(7)
    data_path = Path(args.data)
    seed = best_seed_record(data_path, args.prompt)
    training_text = "\n".join([seed["question"], seed["good_answer"], seed["diagnosis"], seed["follow_up"]])
    model = train_char_markov(training_text, order=args.order)
    generated = generate(model, args.prompt, order=args.order, max_chars=120)
    print(f"最相近主题：{seed['topic']}")
    print(f"基线追问：{seed['follow_up']}")
    print(f"toy LM 生成片段：{generated}")


if __name__ == "__main__":
    main()
