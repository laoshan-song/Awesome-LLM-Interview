from commercial_rag_ticket_assistant.config import Settings
from commercial_rag_ticket_assistant.domain import Document, SourceType, Ticket
from commercial_rag_ticket_assistant.ingestion import Chunker
from commercial_rag_ticket_assistant.rag import RagService
from commercial_rag_ticket_assistant.retrieval import InMemoryHybridIndex
from commercial_rag_ticket_assistant.tickets import TicketAssistant


def build_demo_service() -> RagService:
    documents = [
        Document(
            doc_id="api_timeout_playbook",
            tenant_id="demo",
            title="API 超时排查手册",
            content="# 排查步骤\n客户反馈 API timeout 时，需要先收集请求 ID、接口路径、时间窗口、模型名称和客户端版本，再查询网关日志与模型服务延迟指标。",
            source_type=SourceType.wiki,
            department="support",
            permission_tags={"support"},
        ),
        Document(
            doc_id="rag_index_sync_playbook",
            tenant_id="demo",
            title="知识库索引同步手册",
            content="# 索引同步\n知识库检索不到新文档时，先检查解析任务状态、chunk 数量、embedding 队列积压、向量库 upsert 结果和权限标签。",
            source_type=SourceType.wiki,
            department="platform",
            permission_tags={"support", "platform"},
        ),
    ]
    index = InMemoryHybridIndex()
    chunker = Chunker()
    for document in documents:
        index.upsert(chunker.split(document))
    return RagService(index=index, settings=Settings(confidence_threshold=0.2))


def main() -> None:
    service = build_demo_service()
    answer = service.answer("客户反馈 API timeout 应该收集哪些排查信息？", tenant_id="demo", user_tags={"support"})
    print("RAG answer:")
    print(answer.answer)
    print("citations:", [citation.doc_id for citation in answer.citations])

    ticket = Ticket(
        ticket_id="ticket_001",
        tenant_id="demo",
        subject="API 调用频繁 timeout",
        body="企业客户反馈调用 chat completion 接口经常超时，需要技术支持给出排查步骤。",
        customer_tier="enterprise",
    )
    suggestion = TicketAssistant(service).suggest(ticket, user_tags={"support"})
    print("\nTicket suggestion:")
    print("category:", suggestion.category)
    print("priority:", suggestion.priority.value)
    print("needs_human_review:", suggestion.needs_human_review)
    print(suggestion.suggested_reply)


if __name__ == "__main__":
    main()
