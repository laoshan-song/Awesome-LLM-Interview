import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class Settings:
    app_name: str = "Enterprise Knowledge RAG Ticket Assistant"
    environment: str = "local"
    default_tenant_id: str = "demo"
    retrieval_top_k: int = 5
    confidence_threshold: float = 0.35
    audit_log_path: str = "audit.log"

    def __post_init__(self) -> None:
        self.retrieval_top_k = min(20, max(1, self.retrieval_top_k))
        self.confidence_threshold = min(1.0, max(0.0, self.confidence_threshold))


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("RAG_APP_NAME", Settings.app_name),
        environment=os.getenv("RAG_ENVIRONMENT", Settings.environment),
        default_tenant_id=os.getenv("RAG_DEFAULT_TENANT_ID", Settings.default_tenant_id),
        retrieval_top_k=int(os.getenv("RAG_RETRIEVAL_TOP_K", Settings.retrieval_top_k)),
        confidence_threshold=float(os.getenv("RAG_CONFIDENCE_THRESHOLD", Settings.confidence_threshold)),
        audit_log_path=os.getenv("RAG_AUDIT_LOG_PATH", Settings.audit_log_path),
    )
