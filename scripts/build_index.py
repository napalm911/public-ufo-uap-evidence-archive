#!/usr/bin/env python3
"""
Build vector index from extracted text files.

Usage:
    python scripts/build_index.py
    python scripts/build_index.py --force
    python scripts/build_index.py --text-dir analysis/extracted_text/demo
    python scripts/build_index.py --dry-run
"""

import argparse
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from api.config import settings
from api.services.chunking import chunk_text
from api.services.vector_store import VectorStore


def load_topic_tags() -> dict:
    path = settings.metadata_dir / "topic_tags.json"
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


def find_text_files(text_dir: Path) -> list[Path]:
    files = []
    for pattern in ("*.txt", "*.html"):
        files.extend(text_dir.rglob(pattern))
    return sorted(f for f in files if not f.name.startswith("_"))


def path_to_source(text_path: Path, text_dir: Path) -> tuple[str, str]:
    rel = text_path.relative_to(text_dir)
    parts = rel.parts
    if len(parts) > 1:
        source = parts[0]
    else:
        source = text_dir.name
    return source, text_path.name


def build_index(text_dir: Path, *, force: bool = False, dry_run: bool = False) -> dict:
    topic_tags = load_topic_tags()
    text_files = find_text_files(text_dir)

    all_chunks = []
    sources_seen = set()

    for text_path in text_files:
        try:
            content = text_path.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            print(f"  ⚠ Skipping {text_path}: {e}")
            continue

        source, filename = path_to_source(text_path, text_dir)
        sources_seen.add(source)

        # Match topics from original data path if available
        data_path = f"data/{source}/{filename.replace('.txt', '.pdf')}"
        topics = topic_tags.get(data_path, [])

        chunks = chunk_text(
            content,
            source=source,
            filename=filename,
            topics=topics,
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )
        all_chunks.extend(chunks)

    summary = {
        "files_processed": len(text_files),
        "chunks_created": len(all_chunks),
        "sources": sorted(sources_seen),
    }

    if dry_run:
        print(f"  Dry run: would index {summary['chunks_created']} chunks from {summary['files_processed']} files")
        return summary

    store = VectorStore()
    if force and store.count > 0:
        print("  Resetting existing vector store...")
        store.reset()

    if not all_chunks:
        print("  ⚠ No text chunks to index. Run 'make extract' first.")
        return summary

    batch_size = 32
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i : i + batch_size]
        ids = [f"{c.source}_{c.filename}_{c.chunk_index}" for c in batch]
        texts = [c.text for c in batch]
        metas = [
            {
                "source": c.source,
                "filename": c.filename,
                "chunk_index": c.chunk_index,
                "topics": ",".join(c.topics),
            }
            for c in batch
        ]
        store.add_chunks(ids, texts, metas)

    summary["indexed_chunks"] = store.count
    return summary


def main():
    parser = argparse.ArgumentParser(description="Build vector index from extracted text")
    parser.add_argument("--text-dir", default=str(settings.extracted_text_dir))
    parser.add_argument("--force", action="store_true", help="Reset and rebuild index")
    parser.add_argument("--dry-run", action="store_true", help="Count chunks without indexing")
    args = parser.parse_args()

    text_dir = Path(args.text_dir)
    if not text_dir.exists():
        print(f"Text directory not found: {text_dir}")
        print("Run 'make extract' first, or use 'make demo' for fixture data.")
        sys.exit(1)

    print(f"Building vector index from {text_dir}...")
    settings.chroma_path.mkdir(parents=True, exist_ok=True)

    summary = build_index(text_dir, force=args.force, dry_run=args.dry_run)

    print(f"\n✓ Index build complete")
    print(f"  Files processed: {summary['files_processed']}")
    print(f"  Chunks created: {summary['chunks_created']}")
    print(f"  Sources: {', '.join(summary['sources']) or '(none)'}")
    if "indexed_chunks" in summary:
        print(f"  Total in store: {summary['indexed_chunks']}")


if __name__ == "__main__":
    main()
