"""FastAPI application entry point."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api.config import settings
from api.routes import chat, documents, search, stats

app = FastAPI(
    title="UFO/UAP Evidence Archive",
    description="Semantic search and RAG chat over government UAP documents",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stats.router)
app.include_router(documents.router)
app.include_router(search.router)
app.include_router(chat.router)

# Serve original archive files (read-only)
_data_dir = settings.base_dir / "data"
if _data_dir.exists():
    app.mount("/files", StaticFiles(directory=str(_data_dir)), name="files")


def _frontend_dist() -> Path:
    return settings.frontend_dist


@app.get("/")
async def root():
    index = _frontend_dist() / "index.html"
    if index.exists():
        return FileResponse(index)
    return {
        "message": "UFO/UAP Evidence Archive API",
        "docs": "/docs",
        "hint": "Run 'make build' to serve the frontend",
    }


if _frontend_dist().exists():
    assets = _frontend_dist() / "assets"
    if assets.exists():
        app.mount("/assets", StaticFiles(directory=str(assets)), name="assets")

    @app.get("/{full_path:path}")
    async def spa_fallback(full_path: str):
        """Serve index.html for client-side routes."""
        if full_path.startswith("api/"):
            return {"detail": "Not found"}
        file_path = _frontend_dist() / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        index = _frontend_dist() / "index.html"
        if index.exists():
            return FileResponse(index)
        return {"detail": "Not found"}
