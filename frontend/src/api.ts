import {
  Stats,
  ArchiveFile,
  DocumentListResponse,
  TimelineResponse,
  TopicsResponse,
  DocumentTextResponse,
} from "./types";

export async function fetchStats(): Promise<Stats> {
  const res = await fetch("/api/stats");
  if (!res.ok) throw new Error("Failed to load stats");
  return res.json();
}

export async function fetchHealth(): Promise<{ status: string; indexed_chunks: number }> {
  const res = await fetch("/api/health");
  if (!res.ok) throw new Error("Failed to load health");
  return res.json();
}

export async function fetchDocuments(params: {
  source?: string;
  topic?: string;
  q?: string;
  limit?: number;
  offset?: number;
}): Promise<DocumentListResponse> {
  const qs = new URLSearchParams();
  if (params.source) qs.set("source", params.source);
  if (params.topic) qs.set("topic", params.topic);
  if (params.q) qs.set("q", params.q);
  if (params.limit != null) qs.set("limit", String(params.limit));
  if (params.offset != null) qs.set("offset", String(params.offset));
  const res = await fetch(`/api/documents?${qs}`);
  if (!res.ok) throw new Error("Failed to load documents");
  return res.json();
}

export async function fetchDocument(id: string): Promise<ArchiveFile> {
  const res = await fetch(`/api/documents/${encodeURIComponent(id)}`);
  if (!res.ok) throw new Error("Document not found");
  return res.json();
}

export async function fetchDocumentText(id: string): Promise<DocumentTextResponse> {
  const res = await fetch(`/api/documents/${encodeURIComponent(id)}/text`);
  if (!res.ok) throw new Error("Text not available");
  return res.json();
}

export async function fetchTimeline(): Promise<TimelineResponse> {
  const res = await fetch("/api/timeline");
  if (!res.ok) throw new Error("Failed to load timeline");
  return res.json();
}

export async function fetchTopics(): Promise<TopicsResponse> {
  const res = await fetch("/api/topics");
  if (!res.ok) throw new Error("Failed to load topics");
  return res.json();
}

export async function searchDocuments(query: string, source?: string) {
  const res = await fetch("/api/search", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, source }),
  });
  if (!res.ok) throw new Error("Search failed");
  return res.json();
}

export async function streamChat(
  message: string,
  history: { role: string; content: string }[],
  onToken: (token: string) => void,
  onSources: (sources: unknown[]) => void
): Promise<void> {
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, history, stream: true }),
  });

  if (!res.ok || !res.body) throw new Error("Chat request failed");

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() || "";

    for (const line of lines) {
      if (!line.startsWith("data: ")) continue;
      const payload = line.slice(6).trim();
      if (payload === "[DONE]") return;

      try {
        const event = JSON.parse(payload);
        if (event.type === "token") onToken(event.content);
        if (event.type === "sources") onSources(event.sources);
      } catch {
        // ignore malformed SSE
      }
    }
  }
}
