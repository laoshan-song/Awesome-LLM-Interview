from dataclasses import dataclass, field
from enum import Enum


class SourceType(str, Enum):
    wiki = "wiki"
    pdf = "pdf"
    faq = "faq"
    ticket = "ticket"
    policy = "policy"


class TicketPriority(str, Enum):
    low = "low"
    normal = "normal"
    high = "high"
    urgent = "urgent"


@dataclass
class Document:
    doc_id: str
    tenant_id: str
    title: str
    content: str
    source_type: SourceType
    department: str
    permission_tags: set[str] = field(default_factory=set)
    updated_at: str | None = None


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    tenant_id: str
    title: str
    section_path: str
    content: str
    source_type: SourceType
    department: str
    permission_tags: set[str] = field(default_factory=set)
    token_count: int = 0


@dataclass
class RetrievedChunk:
    chunk: Chunk
    score: float
    reasons: list[str] = field(default_factory=list)


@dataclass
class Citation:
    doc_id: str
    title: str
    section_path: str
    score: float


@dataclass
class Answer:
    answer: str
    confidence: float
    citations: list[Citation]
    refusal: bool = False


@dataclass
class Ticket:
    ticket_id: str
    tenant_id: str
    subject: str
    body: str
    customer_tier: str = "standard"
    priority: TicketPriority = TicketPriority.normal


@dataclass
class TicketSuggestion:
    category: str
    priority: TicketPriority
    summary: str
    suggested_reply: str
    citations: list[Citation]
    needs_human_review: bool
