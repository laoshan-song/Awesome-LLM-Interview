from collections import Counter
from dataclasses import dataclass, field


@dataclass
class FeedbackEvent:
    query: str
    answer: str
    rating: int
    reason: str | None = None
    failure_type: str | None = None


@dataclass
class KnowledgeGap:
    topic: str
    count: int
    examples: list[str] = field(default_factory=list)


class FeedbackStore:
    def __init__(self) -> None:
        self.events: list[FeedbackEvent] = []

    def add(self, event: FeedbackEvent) -> None:
        self.events.append(event)

    def satisfaction_rate(self) -> float:
        if not self.events:
            return 0.0
        positive = sum(1 for event in self.events if event.rating > 0)
        return round(positive / len(self.events), 4)

    def knowledge_gaps(self, limit: int = 10) -> list[KnowledgeGap]:
        counter: Counter[str] = Counter()
        examples: dict[str, list[str]] = {}

        for event in self.events:
            if event.rating >= 0 and event.failure_type not in {"no_answer", "missing_knowledge"}:
                continue
            topic = self._topic(event.query)
            counter[topic] += 1
            examples.setdefault(topic, []).append(event.query)

        return [
            KnowledgeGap(topic=topic, count=count, examples=examples.get(topic, [])[:3])
            for topic, count in counter.most_common(limit)
        ]

    def _topic(self, query: str) -> str:
        normalized = query.strip().replace("\n", " ")
        return normalized[:24] or "unknown"
