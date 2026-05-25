import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { fetchDocument, fetchDocumentText, fetchDocuments } from "../api";
import { ArchiveFile } from "../types";
import { decodeDocId, fileDownloadUrl } from "../lib/docId";
import { formatBytes, searchQueryFromFilename } from "../lib/format";
import { topicLabel } from "../lib/labels";
import Breadcrumbs from "../components/Breadcrumbs";
import { ListSkeleton } from "../components/Skeleton";
import EmptyState from "../components/EmptyState";
import "./DocumentPage.css";

export default function DocumentPage() {
  const { docId } = useParams<{ docId: string }>();
  const navigate = useNavigate();
  const [doc, setDoc] = useState<ArchiveFile | null>(null);
  const [text, setText] = useState<string | null>(null);
  const [related, setRelated] = useState<ArchiveFile[]>([]);
  const [loading, setLoading] = useState(true);
  const [textError, setTextError] = useState(false);

  const path = docId ? decodeDocId(docId) : "";

  useEffect(() => {
    if (!docId) return;
    setLoading(true);
    setTextError(false);

    fetchDocument(path)
      .then((d) => {
        setDoc(d);
        return Promise.all([
          fetchDocumentText(path).then((t) => setText(t.text)).catch(() => {
            setText(null);
            setTextError(true);
          }),
          fetchDocuments({ source: d.source, limit: 10 }).then((r) =>
            setRelated(r.files.filter((f) => f.id !== d.id).slice(0, 5))
          ),
        ]);
      })
      .catch(() => setDoc(null))
      .finally(() => setLoading(false));
  }, [docId, path]);

  if (loading) return <ListSkeleton rows={4} />;

  if (!doc) {
    return <EmptyState message="Document not found." />;
  }

  return (
    <article className="document-page">
      <Breadcrumbs
        items={[
          { label: "Archive", to: "/" },
          { label: doc.source_label, to: `/sources/${doc.source}` },
          { label: doc.filename },
        ]}
      />

      <header className="doc-header">
        <h1>{doc.filename}</h1>
        <p className="doc-meta">
          {doc.source_label} · {doc.extension.replace(".", "").toUpperCase()} ·{" "}
          {formatBytes(doc.size_bytes)}
          {doc.date && <> · {doc.date}</>}
        </p>
      </header>

      {doc.topics.length > 0 && (
        <div className="doc-topics">
          {doc.topics.map((t) => (
            <Link key={t} to={`/topics/${t}`} className="topic-link">
              {topicLabel(t)}
            </Link>
          ))}
        </div>
      )}

      <div className="doc-actions">
        <a href={fileDownloadUrl(doc.path)} className="action-btn" download>
          Download
        </a>
        <button
          className="action-btn primary"
          onClick={() => navigate(`/ask?doc=${encodeURIComponent(doc.filename)}&path=${encodeURIComponent(doc.path)}`)}
        >
          Ask about this
        </button>
        <button
          className="action-btn"
          onClick={() => navigate(`/search?q=${encodeURIComponent(searchQueryFromFilename(doc.filename))}`)}
        >
          Search similar
        </button>
      </div>

      <section className="doc-text-section">
        <h2>Extracted text</h2>
        {text ? (
          <pre className="doc-text">{text}</pre>
        ) : (
          <EmptyState
            message={textError ? "Text not extracted yet." : "No text available."}
            hint="make extract"
          />
        )}
      </section>

      {related.length > 0 && (
        <section className="doc-related">
          <h2>More from {doc.source_label}</h2>
          <ul>
            {related.map((f) => (
              <li key={f.id}>
                <Link to={`/documents/${encodeURIComponent(f.path)}`}>{f.filename}</Link>
              </li>
            ))}
          </ul>
          <Link to={`/sources/${doc.source}`} className="see-all">
            View all →
          </Link>
        </section>
      )}
    </article>
  );
}
