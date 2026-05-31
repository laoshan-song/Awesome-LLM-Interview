import re
from hashlib import sha1

from .domain import Chunk, Document


class Chunker:
    def __init__(self, max_chars: int = 900, overlap_chars: int = 120) -> None:
        self.max_chars = max_chars
        self.overlap_chars = overlap_chars

    def split(self, document: Document) -> list[Chunk]:
        sections = self._split_sections(document.content)
        chunks: list[Chunk] = []
        for section_path, section_text in sections:
            for index, text in enumerate(self._window(section_text)):
                chunk_id = self._chunk_id(document.doc_id, section_path, index, text)
                chunks.append(
                    Chunk(
                        chunk_id=chunk_id,
                        doc_id=document.doc_id,
                        tenant_id=document.tenant_id,
                        title=document.title,
                        section_path=section_path,
                        content=text.strip(),
                        source_type=document.source_type,
                        department=document.department,
                        permission_tags=document.permission_tags,
                        token_count=max(1, len(text) // 4),
                    )
                )
        return chunks

    def _split_sections(self, content: str) -> list[tuple[str, str]]:
        current_title = "root"
        current_lines: list[str] = []
        sections: list[tuple[str, str]] = []

        for line in content.splitlines():
            if re.match(r"^#{1,6}\s+", line):
                if current_lines:
                    sections.append((current_title, "\n".join(current_lines)))
                current_title = line.lstrip("#").strip()
                current_lines = []
            else:
                current_lines.append(line)

        if current_lines:
            sections.append((current_title, "\n".join(current_lines)))

        return [(title, text) for title, text in sections if text.strip()]

    def _window(self, text: str) -> list[str]:
        clean = re.sub(r"\n{3,}", "\n\n", text.strip())
        if len(clean) <= self.max_chars:
            return [clean]

        chunks: list[str] = []
        start = 0
        while start < len(clean):
            end = min(len(clean), start + self.max_chars)
            chunks.append(clean[start:end])
            if end == len(clean):
                break
            start = max(0, end - self.overlap_chars)
        return chunks

    def _chunk_id(self, doc_id: str, section_path: str, index: int, text: str) -> str:
        digest = sha1(f"{doc_id}:{section_path}:{index}:{text}".encode("utf-8")).hexdigest()[:12]
        return f"chk_{digest}"
