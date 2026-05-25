"""Text chunking utilities for vector indexing."""

from dataclasses import dataclass


@dataclass
class TextChunk:
    text: str
    source: str
    filename: str
    chunk_index: int
    topics: list[str]


def chunk_text(
    text: str,
    *,
    source: str,
    filename: str,
    topics: list[str] | None = None,
    chunk_size: int = 800,
    chunk_overlap: int = 120,
) -> list[TextChunk]:
    """Split text into overlapping chunks with metadata."""
    if not text or not text.strip():
        return []

    topics = topics or []
    cleaned = text.strip()
    chunks: list[TextChunk] = []
    start = 0
    index = 0

    while start < len(cleaned):
        end = min(start + chunk_size, len(cleaned))
        if end < len(cleaned):
            # Prefer breaking at paragraph or sentence boundary
            break_at = cleaned.rfind("\n\n", start, end)
            if break_at <= start:
                break_at = cleaned.rfind(". ", start, end)
            if break_at > start:
                end = break_at + 1

        piece = cleaned[start:end].strip()
        if piece:
            chunks.append(
                TextChunk(
                    text=piece,
                    source=source,
                    filename=filename,
                    chunk_index=index,
                    topics=topics,
                )
            )
            index += 1

        if end >= len(cleaned):
            break
        start = max(end - chunk_overlap, start + 1)

    return chunks
