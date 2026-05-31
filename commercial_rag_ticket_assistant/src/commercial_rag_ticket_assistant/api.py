from fastapi import FastAPI, Header
from pydantic import BaseModel

from .audit import AuditLogger
from .config import get_settings
from .domain import Answer, Document, Ticket, TicketSuggestion
from .ingestion import Chunker
from .rag import RagService
from .retrieval import InMemoryHybridIndex
from .tickets import TicketAssistant


settings = get_settings()
index = InMemoryHybridIndex()
chunker = Chunker()
rag_service = RagService(index=index, settings=settings)
ticket_assistant = TicketAssistant(rag_service=rag_service)
audit = AuditLogger(settings.audit_log_path)
app = FastAPI(title=settings.app_name)


class IngestRequest(BaseModel):
    documents: list[Document]


class AskRequest(BaseModel):
    query: str
    tenant_id: str | None = None


class AskResponse(BaseModel):
    result: Answer


class TicketResponse(BaseModel):
    result: TicketSuggestion


def parse_tags(raw: str | None) -> set[str]:
    if not raw:
        return {"public"}
    return {tag.strip() for tag in raw.split(",") if tag.strip()}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}


@app.post("/ingest")
def ingest(request: IngestRequest, x_user_tags: str | None = Header(default=None)) -> dict[str, int]:
    user_tags = parse_tags(x_user_tags)
    chunks = []
    for document in request.documents:
        if document.permission_tags and not document.permission_tags.intersection(user_tags.union({"admin"})):
            continue
        chunks.extend(chunker.split(document))
    index.upsert(chunks)
    audit.log("ingest", {"documents": len(request.documents), "chunks": len(chunks)})
    return {"documents": len(request.documents), "chunks": len(chunks)}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest, x_user_tags: str | None = Header(default=None)) -> AskResponse:
    tenant_id = request.tenant_id or settings.default_tenant_id
    result = rag_service.answer(request.query, tenant_id=tenant_id, user_tags=parse_tags(x_user_tags))
    audit.log("ask", {"tenant_id": tenant_id, "query": request.query, "refusal": result.refusal})
    return AskResponse(result=result)


@app.post("/tickets/suggest", response_model=TicketResponse)
def suggest_ticket(ticket: Ticket, x_user_tags: str | None = Header(default=None)) -> TicketResponse:
    result = ticket_assistant.suggest(ticket, user_tags=parse_tags(x_user_tags))
    audit.log("ticket_suggest", {"tenant_id": ticket.tenant_id, "ticket_id": ticket.ticket_id, "category": result.category})
    return TicketResponse(result=result)
