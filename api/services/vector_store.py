"""ChromaDB vector store wrapper."""

from __future__ import annotations

import chromadb
from chromadb.config import Settings as ChromaSettings

from api.config import settings
from api.services.embeddings import embed_texts


class VectorStore:
    def __init__(self, persist_path=None):
        path = str(persist_path or settings.chroma_path)
        self.client = chromadb.PersistentClient(
            path=path,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(
            name=settings.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    @property
    def count(self) -> int:
        return self.collection.count()

    def reset(self):
        name = settings.collection_name
        try:
            self.client.delete_collection(name)
        except Exception:
            pass
        self.collection = self.client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(
        self,
        ids: list[str],
        texts: list[str],
        metadatas: list[dict],
    ):
        embeddings = embed_texts(texts)
        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(self, query: str, top_k: int | None = None) -> list[dict]:
        k = top_k or settings.top_k
        if self.count == 0:
            return []

        query_embedding = embed_texts([query])[0]
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(k, self.count),
            include=["documents", "metadatas", "distances"],
        )

        hits = []
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        dists = results.get("distances", [[]])[0]

        for doc, meta, dist in zip(docs, metas, dists):
            hits.append(
                {
                    "text": doc,
                    "source": meta.get("source", ""),
                    "filename": meta.get("filename", ""),
                    "chunk_index": meta.get("chunk_index", 0),
                    "topics": meta.get("topics", ""),
                    "score": round(1 - dist, 4),
                }
            )
        return hits
