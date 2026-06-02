from __future__ import annotations

import random

from .diagnosis import diagnose_answer
from .prompt_bank import QUESTIONS


def pick_question(topic: str | None = None) -> tuple[str, str]:
    if topic is None or topic == "random":
        topic = random.choice(sorted(QUESTIONS))
    topic = topic.lower()
    if topic not in QUESTIONS:
        raise ValueError(f"Unknown topic: {topic}")
    return topic, random.choice(QUESTIONS[topic])


def simulate_once(topic: str, answer: str) -> str:
    return diagnose_answer(topic, answer).to_markdown()

