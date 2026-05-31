from commercial_rag_ticket_assistant.config import Settings
from commercial_rag_ticket_assistant.domain import Document, SourceType, Ticket
from commercial_rag_ticket_assistant.ingestion import Chunker
from commercial_rag_ticket_assistant.rag import RagService
from commercial_rag_ticket_assistant.retrieval import InMemoryHybridIndex
from commercial_rag_ticket_assistant.tickets import TicketAssistant


def build_service() -> RagService:
    document = Document(
        doc_id="doc_api_timeout_playbook",
        tenant_id="demo",
        title="API 超时排查手册",
        content="# 排查步骤\n客户反馈 API timeout 时，需要先收集请求 ID、接口路径、时间窗口、模型名称和客户端版本，再查询网关日志与模型服务延迟指标。",
        source_type=SourceType.wiki,
        department="support",
        permission_tags={"support"},
    )
    chunks = Chunker().split(document)
    index = InMemoryHybridIndex()
    index.upsert(chunks)
    return RagService(index=index, settings=Settings(default_tenant_id="demo", confidence_threshold=0.2))


def test_grounded_answer_returns_citation() -> None:
    service = build_service()
    answer = service.answer("客户反馈 API timeout 要收集哪些信息？", tenant_id="demo", user_tags={"support"})

    assert not answer.refusal
    assert answer.citations
    assert answer.citations[0].doc_id == "doc_api_timeout_playbook"


def test_permission_filter_refuses_without_access() -> None:
    service = build_service()
    answer = service.answer("客户反馈 API timeout 要收集哪些信息？", tenant_id="demo", user_tags={"sales"})

    assert answer.refusal
    assert answer.citations == []


def test_ticket_assistant_flags_technical_ticket() -> None:
    service = build_service()
    assistant = TicketAssistant(service)
    suggestion = assistant.suggest(
        Ticket(
            ticket_id="t_001",
            tenant_id="demo",
            subject="API 调用超时",
            body="企业客户反馈 chat completion 接口 timeout，需要排查步骤。",
        ),
        user_tags={"support"},
    )

    assert suggestion.category == "technical_support"
    assert suggestion.citations
