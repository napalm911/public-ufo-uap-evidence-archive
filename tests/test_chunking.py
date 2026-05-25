"""Tests for text chunking."""

from api.services.chunking import chunk_text


def test_chunk_text_basic():
    text = "A" * 1000
    chunks = chunk_text(text, source="odni", filename="report.txt", chunk_size=400, chunk_overlap=50)
    assert len(chunks) >= 2
    assert all(c.source == "odni" for c in chunks)
    assert all(c.filename == "report.txt" for c in chunks)


def test_chunk_text_empty():
    assert chunk_text("", source="x", filename="y") == []
    assert chunk_text("   ", source="x", filename="y") == []


def test_chunk_text_preserves_metadata():
    text = "UAP preliminary assessment. " * 50
    topics = ["aaro_reports"]
    chunks = chunk_text(
        text,
        source="aaro",
        filename="aaro_report.txt",
        topics=topics,
        chunk_size=200,
        chunk_overlap=20,
    )
    assert len(chunks) >= 1
    assert chunks[0].topics == topics
    assert chunks[0].chunk_index == 0
