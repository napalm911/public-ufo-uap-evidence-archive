import { useState, useRef, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { streamChat } from "../api";
import { ChatMessage, SearchResult } from "../types";
import CitationBadge from "./CitationBadge";
import PageHeader from "./PageHeader";
import "./Chat.css";

export default function Chat() {
  const [searchParams] = useSearchParams();
  const docName = searchParams.get("doc");
  const docPath = searchParams.get("path");

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const placeholder = docName
    ? `Ask about ${docName}…`
    : "Ask about UAP evidence in the archive…";

  const sendMessage = async () => {
    let text = input.trim();
    if (!text || loading) return;

    if (docPath && messages.length === 0 && docName && !text.toLowerCase().includes(docName.toLowerCase())) {
      text = `Regarding document ${docName}: ${text}`;
    }

    setInput("");
    setLoading(true);

    const userMsg: ChatMessage = { role: "user", content: text };
    setMessages((prev) => [...prev, userMsg]);

    const assistantMsg: ChatMessage = { role: "assistant", content: "", sources: [] };
    setMessages((prev) => [...prev, assistantMsg]);

    try {
      const history = messages.map((m) => ({ role: m.role, content: m.content }));
      await streamChat(
        text,
        history,
        (token) => {
          setMessages((prev) => {
            const updated = [...prev];
            const last = updated[updated.length - 1];
            if (last.role === "assistant") {
              last.content += token;
            }
            return updated;
          });
        },
        (sources) => {
          setMessages((prev) => {
            const updated = [...prev];
            const last = updated[updated.length - 1];
            if (last.role === "assistant") {
              last.sources = sources as SearchResult[];
            }
            return updated;
          });
        }
      );
    } catch (err) {
      setMessages((prev) => {
        const updated = [...prev];
        const last = updated[updated.length - 1];
        if (last.role === "assistant") {
          last.content = `Error: ${err instanceof Error ? err.message : "Chat failed"}`;
        }
        return updated;
      });
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <section className="chat-section">
      <PageHeader
        title="Ask the Archive"
        subtitle={
          docName
            ? `Focused on: ${docName}`
            : "Chat with government UAP documents using semantic retrieval and DeepSeek."
        }
      />

      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="chat-empty">
            <p>Try asking:</p>
            <ul>
              <li>What did the ODNI Preliminary Assessment conclude about UAPs?</li>
              <li>What legislation relates to UAP disclosure?</li>
              <li>Summarize AARO historical record findings.</li>
            </ul>
          </div>
        )}
        {messages.map((msg, i) => (
          <div key={i} className={`message message-${msg.role}`}>
            <span className="message-role">{msg.role === "user" ? "You" : "Archive"}</span>
            <div className="message-content">
              {msg.content || (loading && i === messages.length - 1 ? "…" : "")}
            </div>
            {msg.sources && msg.sources.length > 0 && (
              <div className="message-sources">
                <p className="sources-label">Sources</p>
                {msg.sources.map((s, j) => (
                  <CitationBadge key={j} source={s} index={j + 1} />
                ))}
              </div>
            )}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <div className="chat-input-row">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          rows={2}
          disabled={loading}
        />
        <button onClick={sendMessage} disabled={loading || !input.trim()}>
          {loading ? "Thinking…" : "Send"}
        </button>
      </div>
    </section>
  );
}
