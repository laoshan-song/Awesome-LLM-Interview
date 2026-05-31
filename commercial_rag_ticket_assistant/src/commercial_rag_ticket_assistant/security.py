from .domain import Chunk, Document


class AccessPolicy:
    def can_read_chunk(self, user_tags: set[str], chunk: Chunk) -> bool:
        if not chunk.permission_tags:
            return True
        return bool(user_tags.intersection(chunk.permission_tags))

    def can_ingest_document(self, user_tags: set[str], document: Document) -> bool:
        if "admin" in user_tags:
            return True
        return document.department in user_tags


def redact_sensitive_text(text: str) -> str:
    digits = 0
    out: list[str] = []
    for char in text:
        if char.isdigit():
            digits += 1
            out.append("*" if digits >= 4 else char)
        else:
            digits = 0
            out.append(char)
    return "".join(out)
