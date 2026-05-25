"""RAG prompt templates."""

SYSTEM_PROMPT = """You are a research assistant for the Public UFO/UAP Government Evidence Archive.
You answer questions using ONLY the retrieved document excerpts provided below.

Rules:
- Cite specific source filenames when referencing evidence (e.g., "According to aaro_report.pdf...").
- If the retrieved context does not contain enough information, say so clearly.
- Do not invent document names, dates, or claims not supported by the context.
- Be precise and neutral. These are official U.S. government and related public documents.
- When comparing sources, note any differences in language or conclusions."""

USER_PROMPT_TEMPLATE = """Retrieved document excerpts:

{context}

---

User question: {question}

Answer based on the excerpts above. Cite source filenames."""


def format_context(chunks: list[dict]) -> str:
    parts = []
    for i, chunk in enumerate(chunks, 1):
        source = chunk.get("source", "unknown")
        filename = chunk.get("filename", "unknown")
        text = chunk.get("text", "")
        parts.append(f"[{i}] Source: {source} | File: {filename}\n{text}")
    return "\n\n".join(parts)
