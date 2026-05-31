from .domain import Ticket, TicketPriority, TicketSuggestion
from .rag import RagService


class TicketAssistant:
    def __init__(self, rag_service: RagService) -> None:
        self.rag_service = rag_service

    def suggest(self, ticket: Ticket, user_tags: set[str]) -> TicketSuggestion:
        query = f"{ticket.subject}\n{ticket.body}"
        answer = self.rag_service.answer(query, tenant_id=ticket.tenant_id, user_tags=user_tags)
        category = self._classify(ticket)
        priority = self._priority(ticket)
        summary = self._summarize(ticket)

        return TicketSuggestion(
            category=category,
            priority=priority,
            summary=summary,
            suggested_reply=self._reply(answer.answer, answer.refusal),
            citations=answer.citations,
            needs_human_review=answer.refusal or priority in {TicketPriority.high, TicketPriority.urgent},
        )

    def _classify(self, ticket: Ticket) -> str:
        text = f"{ticket.subject} {ticket.body}".lower()
        if any(term in text for term in ["error", "timeout", "api", "bug", "报错", "接口", "超时"]):
            return "technical_support"
        if any(term in text for term in ["index", "embedding", "retrieval", "rag", "索引", "向量", "检索", "知识库"]):
            return "knowledge_base"
        if any(term in text for term in ["latency", "throughput", "vllm", "gpu", "延迟", "吞吐", "模型服务"]):
            return "model_serving"
        if any(term in text for term in ["permission", "auth", "token", "权限", "登录", "鉴权"]):
            return "account_access"
        return "general_service"

    def _priority(self, ticket: Ticket) -> TicketPriority:
        text = f"{ticket.subject} {ticket.body}".lower()
        if any(term in text for term in ["production down", "数据丢失", "线上故障", "严重"]):
            return TicketPriority.urgent
        if ticket.customer_tier in {"enterprise", "vip"}:
            return TicketPriority.high
        return ticket.priority

    def _summarize(self, ticket: Ticket) -> str:
        body = ticket.body.replace("\n", " ").strip()
        return f"{ticket.subject}: {body[:180]}"

    def _reply(self, answer: str, refusal: bool) -> str:
        if refusal:
            return "当前知识库证据不足，建议先转人工核验，并补充相关知识条目。"
        return f"您好，已根据当前知识库整理处理建议：\n\n{answer}\n\n如需进一步处理，请补充账号、版本号和复现步骤。"
