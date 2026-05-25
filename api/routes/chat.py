"""RAG chat endpoint with SSE streaming."""

from pydantic import BaseModel, Field

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from api.services.rag import chat_stream, chat_sync

router = APIRouter(prefix="/api", tags=["chat"])


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    history: list[ChatMessage] = Field(default_factory=list)
    stream: bool = True


@router.post("/chat")
async def chat(body: ChatRequest):
    history = [{"role": m.role, "content": m.content} for m in body.history]

    if body.stream:
        return StreamingResponse(
            chat_stream(body.message, history),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )

    return chat_sync(body.message, history)
