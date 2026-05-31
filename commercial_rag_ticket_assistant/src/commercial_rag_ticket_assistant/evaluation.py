from dataclasses import dataclass, field

from .domain import Answer


@dataclass
class GoldenQuestion:
    query: str
    expected_doc_ids: set[str]
    must_include_terms: set[str] = field(default_factory=set)


@dataclass
class EvalResult:
    recall_at_k: float
    citation_accuracy: float
    answer_relevance: float
    failures: list[str]


class RagEvaluator:
    def evaluate(self, answers: list[tuple[GoldenQuestion, Answer]]) -> EvalResult:
        if not answers:
            return EvalResult(recall_at_k=0.0, citation_accuracy=0.0, answer_relevance=0.0, failures=["empty_eval_set"])

        recall_hits = 0
        citation_hits = 0
        relevance_hits = 0
        failures: list[str] = []

        for question, answer in answers:
            cited_doc_ids = {citation.doc_id for citation in answer.citations}
            if question.expected_doc_ids.intersection(cited_doc_ids):
                recall_hits += 1
                citation_hits += 1
            else:
                failures.append(f"missing_expected_doc:{question.query}")

            if all(term in answer.answer for term in question.must_include_terms):
                relevance_hits += 1
            else:
                failures.append(f"missing_required_terms:{question.query}")

        total = len(answers)
        return EvalResult(
            recall_at_k=round(recall_hits / total, 4),
            citation_accuracy=round(citation_hits / total, 4),
            answer_relevance=round(relevance_hits / total, 4),
            failures=failures,
        )
