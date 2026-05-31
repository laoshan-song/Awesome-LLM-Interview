from dataclasses import dataclass
from time import time

from .domain import Answer


@dataclass
class CacheEntry:
    answer: Answer
    expires_at: float


class AnswerCache:
    def __init__(self, ttl_seconds: int = 900) -> None:
        self.ttl_seconds = ttl_seconds
        self._entries: dict[str, CacheEntry] = {}

    def get(self, key: str) -> Answer | None:
        entry = self._entries.get(key)
        if entry is None:
            return None
        if entry.expires_at < time():
            self._entries.pop(key, None)
            return None
        return entry.answer

    def set(self, key: str, answer: Answer) -> None:
        self._entries[key] = CacheEntry(answer=answer, expires_at=time() + self.ttl_seconds)


def cache_key(tenant_id: str, user_tags: set[str], query: str) -> str:
    tags = ",".join(sorted(user_tags))
    return f"{tenant_id}:{tags}:{query.strip().lower()}"
