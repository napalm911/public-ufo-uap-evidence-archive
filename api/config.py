"""Shared configuration loaded from environment."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def _int(name: str, default: int) -> int:
    return int(os.getenv(name, str(default)))


def _str(name: str, default: str) -> str:
    return os.getenv(name, default)


class Settings:
    base_dir: Path = BASE_DIR
    deepseek_api_key: str = _str("DEEPSEEK_API_KEY", "")
    deepseek_base_url: str = _str("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    deepseek_model: str = _str("DEEPSEEK_MODEL", "deepseek-v4-flash")
    embedding_provider: str = _str("EMBEDDING_PROVIDER", "local")
    embedding_model: str = _str("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    openai_api_key: str = _str("OPENAI_API_KEY", "")
    openai_base_url: str = _str("OPENAI_BASE_URL", "https://api.openai.com/v1")
    chroma_path: Path = BASE_DIR / _str("CHROMA_PATH", "./data/vector_store").lstrip("./")
    chunk_size: int = _int("CHUNK_SIZE", 800)
    chunk_overlap: int = _int("CHUNK_OVERLAP", 120)
    top_k: int = _int("TOP_K", 5)
    host: str = _str("HOST", "0.0.0.0")
    port: int = _int("PORT", 8000)
    cors_origins: list[str] = [
        o.strip() for o in _str("CORS_ORIGINS", "http://localhost:5173,http://localhost:8000").split(",") if o.strip()
    ]
    metadata_dir: Path = BASE_DIR / "metadata"
    extracted_text_dir: Path = BASE_DIR / "analysis" / "extracted_text"
    frontend_dist: Path = BASE_DIR / "frontend" / "dist"
    collection_name: str = "uap_documents"


settings = Settings()
