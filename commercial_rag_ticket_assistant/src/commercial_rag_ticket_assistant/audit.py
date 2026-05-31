import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .security import redact_sensitive_text


class AuditLogger:
    def __init__(self, path: str) -> None:
        self.path = Path(path)

    def log(self, event_type: str, payload: dict[str, Any]) -> None:
        event = {
            "ts": datetime.now(UTC).isoformat(),
            "event_type": event_type,
            "payload": self._redact_payload(payload),
        }
        with self.path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(event, ensure_ascii=False) + "\n")

    def _redact_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        redacted: dict[str, Any] = {}
        for key, value in payload.items():
            if isinstance(value, str):
                redacted[key] = redact_sensitive_text(value)
            else:
                redacted[key] = value
        return redacted
