from __future__ import annotations

import hashlib
import json
import math
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


ROOT = Path(__file__).resolve().parent
DEFAULT_INDEX_PATH = ROOT.parent / "assets" / "local_pdf_rag_index.json"


def env_bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).lower() in {"1", "true", "yes", "on"}


def env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, default))
    except ValueError:
        return default


def env_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, default))
    except ValueError:
        return default


EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-zh-v1.5")
QUERY_PREFIX = os.getenv("QUERY_PREFIX", "为这个句子生成表示以用于检索相关文章：")
RERANKER_MODEL = os.getenv("RERANKER_MODEL", "BAAI/bge-reranker-v2-m3")
ENABLE_RERANKER = env_bool("ENABLE_RERANKER", False)
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
TOP_K = env_int("TOP_K", 8)
CANDIDATE_K = env_int("CANDIDATE_K", 60)
HYBRID_ALPHA = env_float("HYBRID_ALPHA", 0.68)
ALLOW_ORIGINS = [origin.strip() for origin in os.getenv("ALLOW_ORIGINS", "*").split(",") if origin.strip()]
INDEX_PATH = Path(os.getenv("RAG_INDEX_PATH", DEFAULT_INDEX_PATH)).resolve()
CACHE_DIR = Path(os.getenv("RAG_CACHE_DIR", ROOT / "data")).resolve()


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").lower()).strip()


def tokenize(text: str) -> list[str]:
    normalized = normalize_text(text)
    latin = re.findall(r"[a-z0-9_+\-]{2,}", normalized)
    cjk_terms: list[str] = []
    for word in re.findall(r"[\u4e00-\u9fff]{2,}", normalized):
        cjk_terms.extend(word[i : i + 2] for i in range(max(0, len(word) - 1)))
    return list(dict.fromkeys(latin + cjk_terms))


def split_sentences(text: str) -> list[str]:
    cleaned = re.sub(r"[\x00-\x1f]+", " ", text or "")
    parts = re.split(r"(?<=[。！？?；;])\s+|\n+|\s{2,}", cleaned)
    sentences = [part.strip() for part in parts if 24 <= len(part.strip()) <= 240]
    return sentences or [cleaned[:220].strip()]


@dataclass(frozen=True)
class Chunk:
    id: str
    doc_id: str
    doc_title: str
    doc_path: str
    pdf_url: str
    page: int
    topic: str
    chunk_index: int
    text: str

    @classmethod
    def from_raw(cls, raw: dict[str, Any]) -> "Chunk":
        return cls(
            id=str(raw.get("id", "")),
            doc_id=str(raw.get("docId", "")),
            doc_title=str(raw.get("docTitle", "")),
            doc_path=str(raw.get("docPath", "")),
            pdf_url=str(raw.get("pdfUrl", "")),
            page=int(raw.get("page") or 1),
            topic=str(raw.get("topic", "general")),
            chunk_index=int(raw.get("chunkIndex") or 0),
            text=str(raw.get("text", "")),
        )


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    top_k: int = Field(default=TOP_K, ge=1, le=20)
    candidate_k: int = Field(default=CANDIDATE_K, ge=10, le=200)
    use_llm: bool = Field(default=True)


class Citation(BaseModel):
    title: str
    page: int
    text: str
    pdf_url: str
    topic: str
    score: float
    vector_score: float
    bm25_score: float


class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation]
    query: str
    embedding_model: str
    reranker_model: str | None
    mode: str


class HealthResponse(BaseModel):
    ok: bool
    document_count: int
    chunk_count: int
    embedding_model: str
    reranker_enabled: bool
    llm_enabled: bool


class RagEngine:
    def __init__(self, index_path: Path) -> None:
        self.index_path = index_path
        self.chunks: list[Chunk] = []
        self.embeddings: np.ndarray | None = None
        self.embedding_model: Any = None
        self.reranker: Any = None
        self.doc_freq: dict[str, int] = {}
        self.tokenized_chunks: list[list[str]] = []
        self.avg_doc_len = 1.0
        self.document_count = 0

    def load(self) -> None:
        if not self.index_path.exists():
            raise FileNotFoundError(f"RAG index not found: {self.index_path}")
        data = json.loads(self.index_path.read_text(encoding="utf-8"))
        self.document_count = int(data.get("documentCount") or 0)
        self.chunks = [Chunk.from_raw(raw) for raw in data.get("chunks", []) if raw.get("text")]
        if not self.chunks:
            raise ValueError("RAG index has no chunks")
        self._build_bm25()
        self._load_embedding_model()
        self._load_or_build_embeddings()
        if ENABLE_RERANKER:
            self._load_reranker()

    def _load_embedding_model(self) -> None:
        from sentence_transformers import SentenceTransformer

        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)

    def _load_reranker(self) -> None:
        from sentence_transformers import CrossEncoder

        self.reranker = CrossEncoder(RERANKER_MODEL)

    def _cache_path(self) -> Path:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        signature = f"{self.index_path}:{self.index_path.stat().st_mtime_ns}:{len(self.chunks)}:{EMBEDDING_MODEL}"
        digest = hashlib.sha256(signature.encode("utf-8")).hexdigest()[:16]
        safe_model = re.sub(r"[^a-zA-Z0-9_.-]+", "_", EMBEDDING_MODEL)
        return CACHE_DIR / f"embeddings_{safe_model}_{digest}.npz"

    def _load_or_build_embeddings(self) -> None:
        cache_path = self._cache_path()
        if cache_path.exists():
            self.embeddings = np.load(cache_path)["embeddings"].astype(np.float32)
            return
        texts = [self._embedding_text(chunk) for chunk in self.chunks]
        vectors = self.embedding_model.encode(
            texts,
            batch_size=32,
            normalize_embeddings=True,
            show_progress_bar=True,
        )
        self.embeddings = np.asarray(vectors, dtype=np.float32)
        np.savez_compressed(cache_path, embeddings=self.embeddings)

    def _embedding_text(self, chunk: Chunk) -> str:
        return f"标题：{chunk.doc_title}\n主题：{chunk.topic}\n正文：{chunk.text}"

    def _build_bm25(self) -> None:
        self.tokenized_chunks = []
        self.doc_freq = {}
        lengths: list[int] = []
        for chunk in self.chunks:
            tokens = tokenize(f"{chunk.doc_title} {chunk.topic} {chunk.text}")
            self.tokenized_chunks.append(tokens)
            lengths.append(len(tokens))
            for token in set(tokens):
                self.doc_freq[token] = self.doc_freq.get(token, 0) + 1
        self.avg_doc_len = max(1.0, sum(lengths) / max(1, len(lengths)))

    def _bm25_scores(self, query: str) -> np.ndarray:
        query_terms = tokenize(query)
        scores = np.zeros(len(self.chunks), dtype=np.float32)
        if not query_terms:
            return scores
        n = len(self.chunks)
        k1 = 1.5
        b = 0.72
        for i, tokens in enumerate(self.tokenized_chunks):
            if not tokens:
                continue
            doc_len = len(tokens)
            freqs: dict[str, int] = {}
            for token in tokens:
                freqs[token] = freqs.get(token, 0) + 1
            score = 0.0
            for term in query_terms:
                tf = freqs.get(term, 0)
                if not tf:
                    continue
                df = self.doc_freq.get(term, 0)
                idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
                denom = tf + k1 * (1 - b + b * doc_len / self.avg_doc_len)
                score += idf * (tf * (k1 + 1)) / denom
            scores[i] = score
        return scores

    @staticmethod
    def _minmax(scores: np.ndarray) -> np.ndarray:
        if not np.any(scores):
            return scores
        lo = float(np.min(scores))
        hi = float(np.max(scores))
        if hi - lo < 1e-8:
            return np.ones_like(scores)
        return (scores - lo) / (hi - lo)

    def retrieve(self, query: str, top_k: int, candidate_k: int) -> list[dict[str, Any]]:
        if self.embeddings is None:
            raise RuntimeError("Embeddings are not initialized")
        query_for_embedding = f"{QUERY_PREFIX}{query}" if QUERY_PREFIX else query
        query_embedding = self.embedding_model.encode([query_for_embedding], normalize_embeddings=True)[0].astype(np.float32)
        vector_scores = self.embeddings @ query_embedding
        bm25_scores = self._bm25_scores(query)
        hybrid_scores = HYBRID_ALPHA * self._minmax(vector_scores) + (1 - HYBRID_ALPHA) * self._minmax(bm25_scores)

        candidate_count = min(candidate_k, len(self.chunks))
        candidate_indices = np.argpartition(-hybrid_scores, candidate_count - 1)[:candidate_count]
        candidates = [
            {
                "index": int(idx),
                "chunk": self.chunks[int(idx)],
                "score": float(hybrid_scores[int(idx)]),
                "vector_score": float(vector_scores[int(idx)]),
                "bm25_score": float(bm25_scores[int(idx)]),
            }
            for idx in candidate_indices
        ]
        candidates.sort(key=lambda item: item["score"], reverse=True)

        if self.reranker is not None and candidates:
            pairs = [[query, item["chunk"].text] for item in candidates]
            rerank_scores = self.reranker.predict(pairs)
            for item, rerank_score in zip(candidates, rerank_scores):
                item["score"] = 0.35 * item["score"] + 0.65 * float(rerank_score)
            candidates.sort(key=lambda item: item["score"], reverse=True)

        deduped: list[dict[str, Any]] = []
        doc_counts: dict[str, int] = {}
        for item in candidates:
            doc_id = item["chunk"].doc_id
            if doc_counts.get(doc_id, 0) >= 2:
                continue
            doc_counts[doc_id] = doc_counts.get(doc_id, 0) + 1
            deduped.append(item)
            if len(deduped) >= top_k:
                break
        return deduped

    def build_extractive_answer(self, query: str, hits: list[dict[str, Any]]) -> str:
        terms = tokenize(query)
        lines = [f"基于检索到的 PDF 证据，关于“{query}”可以这样回答："]
        for i, hit in enumerate(hits[:5], start=1):
            chunk = hit["chunk"]
            sentence = self._best_sentence(chunk.text, terms)
            lines.append(f"[{i}] {sentence}（{chunk.doc_title}，第 {chunk.page} 页）")
        lines.append("以上回答只来自命中的 PDF 片段；如果用于面试复述，建议打开引用页核对上下文。")
        return "\n".join(lines)

    @staticmethod
    def _best_sentence(text: str, terms: list[str]) -> str:
        sentences = split_sentences(text)
        scored = []
        for sentence in sentences:
            normalized = normalize_text(sentence)
            score = sum(normalized.count(term) for term in terms)
            scored.append((score, len(sentence), sentence))
        scored.sort(key=lambda item: (-item[0], item[1]))
        return scored[0][2]


engine = RagEngine(INDEX_PATH)
app = FastAPI(title="Awesome LLM Interview RAG API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS if ALLOW_ORIGINS != ["*"] else ["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    engine.load()


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        ok=True,
        document_count=engine.document_count,
        chunk_count=len(engine.chunks),
        embedding_model=EMBEDDING_MODEL,
        reranker_enabled=engine.reranker is not None,
        llm_enabled=bool(os.getenv("OPENAI_API_KEY")),
    )


@app.post("/api/rag/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest) -> QueryResponse:
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="query is required")
    hits = engine.retrieve(query, top_k=request.top_k, candidate_k=request.candidate_k)
    if not hits:
        return QueryResponse(
            answer="没有检索到足够相关的 PDF 证据。请换成更具体的关键词。",
            citations=[],
            query=query,
            embedding_model=EMBEDDING_MODEL,
            reranker_model=RERANKER_MODEL if engine.reranker is not None else None,
            mode="empty",
        )

    citations = [
        Citation(
            title=hit["chunk"].doc_title,
            page=hit["chunk"].page,
            text=hit["chunk"].text[:900],
            pdf_url=hit["chunk"].pdf_url,
            topic=hit["chunk"].topic,
            score=round(float(hit["score"]), 6),
            vector_score=round(float(hit["vector_score"]), 6),
            bm25_score=round(float(hit["bm25_score"]), 6),
        )
        for hit in hits
    ]

    mode = "extractive"
    answer = engine.build_extractive_answer(query, hits)
    if request.use_llm and os.getenv("OPENAI_API_KEY"):
        answer = await generate_llm_answer(query, citations)
        mode = "llm"

    return QueryResponse(
        answer=answer,
        citations=citations,
        query=query,
        embedding_model=EMBEDDING_MODEL,
        reranker_model=RERANKER_MODEL if engine.reranker is not None else None,
        mode=mode,
    )


async def generate_llm_answer(query: str, citations: list[Citation]) -> str:
    from openai import AsyncOpenAI

    client = AsyncOpenAI()
    context = "\n\n".join(
        f"[{i}] 标题：{item.title}\n页码：{item.page}\n片段：{item.text}"
        for i, item in enumerate(citations[:6], start=1)
    )
    response = await client.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=0.1,
        messages=[
            {
                "role": "system",
                "content": "你是严谨的 LLM 面试辅导助手。只能使用给定 PDF 片段回答，必须用 [1] 这样的编号引用证据；证据不足时直接说明不足。",
            },
            {
                "role": "user",
                "content": f"问题：{query}\n\nPDF 证据：\n{context}\n\n请给出适合面试复述的中文回答。",
            },
        ],
    )
    return response.choices[0].message.content or ""
