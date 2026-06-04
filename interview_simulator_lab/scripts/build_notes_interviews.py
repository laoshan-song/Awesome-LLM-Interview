from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


QUESTION_HEADING = "## 面试高频考点"
STOP_HEADINGS = ("## 一句话", "## 总览", "## 一、", "## 1.", "## 为什么", "---")


def clean_inline(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text.strip()


def infer_topic(path: Path) -> str:
    stem = path.stem.lower()
    if "rag" in stem:
        return "rag"
    if "lora" in stem or "peft" in stem:
        return "lora"
    if "kv_cache" in stem or "kv" in stem:
        return "kv_cache"
    if "sft" in stem or "微调" in stem:
        return "sft"
    if "agent" in stem or "mcp" in stem:
        return "agent"
    if "量化" in stem:
        return "quantization"
    if "解码" in stem:
        return "decoding"
    if "transformer" in stem:
        return "transformer"
    return path.parent.name.split("_", 1)[-1].lower()


def extract_title(text: str, path: Path) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return clean_inline(line[2:])
    return path.stem


def extract_questions(text: str) -> list[str]:
    lines = text.splitlines()
    in_section = False
    questions: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped == QUESTION_HEADING:
            in_section = True
            continue
        if in_section and stripped.startswith(STOP_HEADINGS):
            break
        if in_section and stripped.startswith("- "):
            question = clean_inline(stripped[2:])
            if question.endswith("？") or question.endswith("?"):
                questions.append(question)
    return questions


def extract_answer_material(text: str) -> str:
    lines = []
    skip = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("|") or stripped.startswith("!["):
            skip = not skip if stripped.startswith("```") else skip
            continue
        if skip or not stripped:
            continue
        if stripped.startswith("#") or stripped.startswith("- ") or re.match(r"^\d+\.", stripped):
            continue
        if stripped.startswith(">"):
            stripped = stripped.lstrip("> ").strip()
        if len(stripped) >= 18 and not stripped.startswith(("图源", "平台", "论文")):
            lines.append(clean_inline(stripped))
        if len("".join(lines)) > 420:
            break
    return " ".join(lines)[:520]


def weak_answer_for(topic: str, title: str) -> str:
    weak_map = {
        "rag": "RAG 就是把资料塞给模型，所以基本不会幻觉。",
        "lora": "LoRA 是一种量化压缩方法，把模型变小就能省显存。",
        "kv_cache": "KV Cache 就是缓存模型最终回答，下一次相同问题直接复用。",
        "sft": "SFT 只要数据越多越好，模型就会自然变聪明。",
        "agent": "Agent 就是让大模型自动调用工具，所以能自动完成复杂任务。",
        "quantization": "量化就是无损压缩模型，bit 越低速度和效果都会越好。",
        "decoding": "解码参数只是控制模型聪不聪明，temperature 越高越会推理。",
        "transformer": "Transformer 主要就是 attention，其他模块不太重要。",
    }
    return weak_map.get(topic, f"{title} 主要就是背概念，知道定义就可以了。")


def diagnosis_for(topic: str, title: str) -> str:
    return (
        f"回答过于绝对或停留在定义层面，没有展开 {title} 的核心机制、工程边界和评估方式。"
        "建议先解释原理，再补充典型失败场景、关键指标和线上排障思路。"
    )


def follow_up_for(topic: str, title: str) -> str:
    followups = {
        "rag": "如果答案错了，你会如何区分是召回、重排、上下文拼接还是生成阶段的问题？",
        "lora": "如果 LoRA 训练集效果好但泛化差，你会从 rank、数据和 target modules 上怎么排查？",
        "kv_cache": "长上下文和高并发同时出现时，你会如何估算并降低 KV Cache 显存？",
        "sft": "如果 SFT 后模型变得模板化，你会如何调整数据和训练配置？",
        "agent": "如何防止 Agent 把网页或工具返回里的恶意指令当成系统指令执行？",
    }
    return followups.get(topic, f"你能举一个 {title} 在线上系统里的失败案例和排障步骤吗？")


def build_record(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    title = extract_title(text, path)
    topic = infer_topic(path)
    material = extract_answer_material(text)
    questions = extract_questions(text)[:3]
    records = []
    for question in questions:
        records.append(
            {
                "topic": topic,
                "source": str(path),
                "question": question,
                "good_answer": material
                or f"{title} 的回答应覆盖核心定义、关键机制、工程取舍、常见误区和评估方式。",
                "weak_answer": weak_answer_for(topic, title),
                "diagnosis": diagnosis_for(topic, title),
                "follow_up": follow_up_for(topic, title),
            }
        )
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Build interview seed data from markdown notes.")
    parser.add_argument("--notes-root", default="../notes")
    parser.add_argument("--output", default="data/notes_interviews.jsonl")
    parser.add_argument("--max-per-file", type=int, default=3)
    args = parser.parse_args()

    notes_root = Path(args.notes_root)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    records = []
    for path in sorted(notes_root.glob("[0-9][0-9]_*/*.md")):
        if "assets" in path.parts:
            continue
        records.extend(build_record(path)[: args.max_per_file])

    with output.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Wrote {len(records)} records to {output}")


if __name__ == "__main__":
    main()
