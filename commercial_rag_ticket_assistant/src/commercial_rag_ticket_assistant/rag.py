from .config import Settings
from .domain import Answer, Citation, RetrievedChunk
from .retrieval import InMemoryHybridIndex


class RagService:
    def __init__(self, index: InMemoryHybridIndex, settings: Settings) -> None:
        self.index = index
        self.settings = settings

    def answer(self, query: str, tenant_id: str, user_tags: set[str]) -> Answer:
        retrieved = self.index.search(query, tenant_id=tenant_id, user_tags=user_tags, top_k=self.settings.retrieval_top_k)
        retrieved = self._filter_weak_evidence(retrieved)
        confidence = self._confidence(retrieved)
        citations = [
            Citation(
                doc_id=item.chunk.doc_id,
                title=item.chunk.title,
                section_path=item.chunk.section_path,
                score=round(item.score, 4),
            )
            for item in retrieved[:3]
        ]

        if confidence < self.settings.confidence_threshold:
            return Answer(
                answer="当前知识库没有足够依据回答该问题，建议补充资料或转人工处理。",
                confidence=confidence,
                citations=citations,
                refusal=True,
            )

        evidence = "\n".join(f"- {item.chunk.title} / {item.chunk.section_path}: {item.chunk.content}" for item in retrieved[:3])
        answer = self._compose_grounded_answer(query, evidence)
        return Answer(answer=answer, confidence=confidence, citations=citations)

    def _confidence(self, retrieved: list[RetrievedChunk]) -> float:
        if not retrieved:
            return 0.0
        top = retrieved[0].score
        second = retrieved[1].score if len(retrieved) > 1 else 0.0
        margin = max(0.0, top - second)
        return round(min(1.0, 0.35 + top / 8 + margin / 4), 4)

    def _filter_weak_evidence(self, retrieved: list[RetrievedChunk]) -> list[RetrievedChunk]:
        if not retrieved:
            return []
        top_score = retrieved[0].score
        threshold = max(0.08, top_score * 0.45)
        return [item for item in retrieved if item.score >= threshold]

    def _compose_grounded_answer(self, query: str, evidence: str) -> str:
        return (
            f"基于已检索到的企业知识，针对“{query}”的处理建议如下：\n"
            f"{self._summarize_evidence(evidence)}\n\n"
            "回答已依据上方证据生成；如果业务场景涉及权限变更、客户数据或生产故障，建议转人工复核。"
        )

    def _summarize_evidence(self, evidence: str) -> str:
        lines = [line.strip("- ").strip() for line in evidence.splitlines() if line.strip()]
        if not lines:
            return "未找到可用证据。"
        return "\n".join(f"{index}. {line[:220]}" for index, line in enumerate(lines[:3], start=1))
