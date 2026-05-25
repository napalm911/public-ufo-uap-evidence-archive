import { useState, useEffect, useRef } from "react";
import { useSearchParams } from "react-router-dom";
import { searchDocuments } from "../api";
import { SearchResult } from "../types";
import CitationBadge from "./CitationBadge";
import PageHeader from "./PageHeader";
import "./SearchPanel.css";

export default function SearchPanel() {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialQ = searchParams.get("q") || "";
  const inputRef = useRef<HTMLInputElement>(null);

  const [query, setQuery] = useState(initialQ);
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const runSearch = async (q: string) => {
    const trimmed = q.trim();
    if (!trimmed || loading) return;

    setLoading(true);
    setSearched(true);
    setSearchParams(trimmed ? { q: trimmed } : {});
    try {
      const data = await searchDocuments(trimmed);
      setResults(data.results || []);
    } catch {
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (initialQ) {
      runSearch(initialQ);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "/" && document.activeElement?.tagName !== "INPUT") {
        e.preventDefault();
        inputRef.current?.focus();
      }
      if (e.key === "Escape" && document.activeElement === inputRef.current) {
        setQuery("");
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      e.preventDefault();
      runSearch(query);
    }
  };

  return (
    <section className="search-section">
      <PageHeader
        title="Semantic Search"
        subtitle="Find relevant document excerpts by meaning, not just keywords. Press / to focus."
      />

      <div className="search-input-row">
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="e.g. transmedium capability, non-human intelligence…"
          disabled={loading}
        />
        <button onClick={() => runSearch(query)} disabled={loading || !query.trim()}>
          {loading ? "Searching…" : "Search"}
        </button>
      </div>

      {searched && (
        <div className="search-results">
          {results.length === 0 ? (
            <p className="no-results">
              No results found. Try a different query or run <code>make index</code>.
            </p>
          ) : (
            results.map((r, i) => <CitationBadge key={i} source={r} index={i + 1} />)
          )}
        </div>
      )}
    </section>
  );
}
