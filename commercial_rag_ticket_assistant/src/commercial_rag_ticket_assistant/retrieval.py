import math
import re
from collections import Counter, defaultdict

from .domain import Chunk, RetrievedChunk
from .security import AccessPolicy


ASCII_PATTERN = re.compile(r"[a-zA-Z0-9_]+")
CHINESE_PATTERN = re.compile(r"[\u4e00-\u9fff]+")


def tokenize(text: str) -> list[str]:
    tokens = [token.lower() for token in ASCII_PATTERN.findall(text)]
    for segment in CHINESE_PATTERN.findall(text):
        chars = list(segment)
        tokens.extend(chars)
        tokens.extend("".join(chars[index : index + 2]) for index in range(max(0, len(chars) - 1)))
        tokens.extend("".join(chars[index : index + 3]) for index in range(max(0, len(chars) - 2)))
    return tokens


class InMemoryHybridIndex:
    def __init__(self, access_policy: AccessPolicy | None = None) -> None:
        self.access_policy = access_policy or AccessPolicy()
        self.chunks: dict[str, Chunk] = {}
        self.term_freqs: dict[str, Counter[str]] = {}
        self.doc_freqs: Counter[str] = Counter()
        self.embeddings: dict[str, list[float]] = {}

    def upsert(self, chunks: list[Chunk]) -> None:
        for chunk in chunks:
            old_terms = set(self.term_freqs.get(chunk.chunk_id, Counter()))
            for term in old_terms:
                self.doc_freqs[term] -= 1

            terms = Counter(tokenize(chunk.title + " " + chunk.section_path + " " + chunk.content))
            self.chunks[chunk.chunk_id] = chunk
            self.term_freqs[chunk.chunk_id] = terms
            self.embeddings[chunk.chunk_id] = self._embed(terms)
            for term in terms:
                self.doc_freqs[term] += 1

    def search(self, query: str, tenant_id: str, user_tags: set[str], top_k: int = 5) -> list[RetrievedChunk]:
        query_terms = Counter(tokenize(query))
        query_embedding = self._embed(query_terms)
        scored: list[RetrievedChunk] = []

        for chunk_id, chunk in self.chunks.items():
            if chunk.tenant_id != tenant_id:
                continue
            if not self.access_policy.can_read_chunk(user_tags, chunk):
                continue

            bm25 = self._bm25(query_terms, chunk_id)
            dense = self._cosine(query_embedding, self.embeddings[chunk_id])
            score = 0.58 * bm25 + 0.42 * dense
            reasons = self._reasons(query_terms, chunk)
            if score > 0:
                scored.append(RetrievedChunk(chunk=chunk, score=score, reasons=reasons))

        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:top_k]

    def _bm25(self, query_terms: Counter[str], chunk_id: str, k1: float = 1.2, b: float = 0.75) -> float:
        terms = self.term_freqs[chunk_id]
        avg_len = max(1.0, sum(sum(tf.values()) for tf in self.term_freqs.values()) / max(1, len(self.term_freqs)))
        doc_len = max(1, sum(terms.values()))
        total_docs = max(1, len(self.term_freqs))
        score = 0.0

        for term, query_count in query_terms.items():
            tf = terms.get(term, 0)
            if tf == 0:
                continue
            df = max(1, self.doc_freqs.get(term, 0))
            idf = math.log(1 + (total_docs - df + 0.5) / (df + 0.5))
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * doc_len / avg_len)
            score += query_count * idf * numerator / denominator
        return score

    def _embed(self, terms: Counter[str]) -> list[float]:
        vector = [0.0] * 128
        for term, count in terms.items():
            bucket = hash(term) % len(vector)
            vector[bucket] += float(count)
        norm = math.sqrt(sum(value * value for value in vector))
        if not norm:
            return vector
        return [value / norm for value in vector]

    def _cosine(self, left: list[float], right: list[float]) -> float:
        left_norm = math.sqrt(sum(value * value for value in left))
        right_norm = math.sqrt(sum(value * value for value in right))
        denominator = left_norm * right_norm
        if denominator == 0:
            return 0.0
        return sum(a * b for a, b in zip(left, right)) / denominator

    def _reasons(self, query_terms: Counter[str], chunk: Chunk) -> list[str]:
        chunk_terms = set(tokenize(chunk.title + " " + chunk.section_path + " " + chunk.content))
        matches = sorted(set(query_terms).intersection(chunk_terms))
        return [f"keyword:{term}" for term in matches[:5]]


def reciprocal_rank_fusion(result_sets: list[list[RetrievedChunk]], top_k: int = 5, k: int = 60) -> list[RetrievedChunk]:
    fused_scores: defaultdict[str, float] = defaultdict(float)
    chunk_by_id: dict[str, RetrievedChunk] = {}

    for results in result_sets:
        for rank, item in enumerate(results, start=1):
            fused_scores[item.chunk.chunk_id] += 1 / (k + rank)
            chunk_by_id[item.chunk.chunk_id] = item

    fused = [
        RetrievedChunk(chunk=chunk_by_id[chunk_id].chunk, score=score, reasons=chunk_by_id[chunk_id].reasons)
        for chunk_id, score in fused_scores.items()
    ]
    fused.sort(key=lambda item: item.score, reverse=True)
    return fused[:top_k]
