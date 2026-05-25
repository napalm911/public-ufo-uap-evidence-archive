"""RAG orchestration: retrieve context and generate responses."""

from __future__ import annotations

import json
from typing import AsyncIterator

from openai import OpenAI

from api.config import settings
from api.services.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE, format_context
from api.services.vector_store import VectorStore


def get_llm_client() -> OpenAI:
    return OpenAI(
        api_key=settings.deepseek_api_key,
        base_url=settings.deepseek_base_url,
    )


def retrieve(query: str, top_k: int | None = None) -> list[dict]:
    store = VectorStore()
    return store.search(query, top_k=top_k)


def chat_sync(query: str, history: list[dict] | None = None) -> dict:
    """Non-streaming chat for tests."""
    chunks = retrieve(query)
    context = format_context(chunks)

    if not settings.deepseek_api_key:
        return {
            "answer": "DeepSeek API key not configured. Set DEEPSEEK_API_KEY in .env.",
            "sources": chunks,
        }

    client = get_llm_client()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        for msg in history[-6:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append(
        {
            "role": "user",
            "content": USER_PROMPT_TEMPLATE.format(context=context, question=query),
        }
    )

    response = client.chat.completions.create(
        model=settings.deepseek_model,
        messages=messages,
        stream=False,
    )
    answer = response.choices[0].message.content or ""
    return {"answer": answer, "sources": chunks}


async def chat_stream(query: str, history: list[dict] | None = None) -> AsyncIterator[str]:
    """Stream SSE events: token chunks, then sources."""
    chunks = retrieve(query)
    context = format_context(chunks)

    if not settings.deepseek_api_key:
        yield f"data: {json.dumps({'type': 'token', 'content': 'DeepSeek API key not configured. Set DEEPSEEK_API_KEY in .env.'})}\n\n"
        yield f"data: {json.dumps({'type': 'sources', 'sources': chunks})}\n\n"
        yield "data: [DONE]\n\n"
        return

    client = get_llm_client()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        for msg in history[-6:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append(
        {
            "role": "user",
            "content": USER_PROMPT_TEMPLATE.format(context=context, question=query),
        }
    )

    stream = client.chat.completions.create(
        model=settings.deepseek_model,
        messages=messages,
        stream=True,
    )

    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield f"data: {json.dumps({'type': 'token', 'content': delta})}\n\n"

    yield f"data: {json.dumps({'type': 'sources', 'sources': chunks})}\n\n"
    yield "data: [DONE]\n\n"
