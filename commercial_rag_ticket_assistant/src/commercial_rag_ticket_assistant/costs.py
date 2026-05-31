from dataclasses import dataclass


@dataclass
class ModelPrice:
    input_per_1k: float
    output_per_1k: float


@dataclass
class UsageRecord:
    request_id: str
    input_tokens: int
    output_tokens: int
    cache_hit: bool = False


class CostTracker:
    def __init__(self, price: ModelPrice) -> None:
        self.price = price
        self.records: list[UsageRecord] = []

    def add(self, record: UsageRecord) -> None:
        self.records.append(record)

    def estimate(self, record: UsageRecord) -> float:
        input_tokens = 0 if record.cache_hit else record.input_tokens
        return round(input_tokens / 1000 * self.price.input_per_1k + record.output_tokens / 1000 * self.price.output_per_1k, 6)

    def total_cost(self) -> float:
        return round(sum(self.estimate(record) for record in self.records), 6)

    def cache_hit_rate(self) -> float:
        if not self.records:
            return 0.0
        hits = sum(1 for record in self.records if record.cache_hit)
        return round(hits / len(self.records), 4)
