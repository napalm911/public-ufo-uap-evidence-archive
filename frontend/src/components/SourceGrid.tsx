import { Link } from "react-router-dom";
import { Stats } from "../types";
import "./SourceGrid.css";

interface Props {
  stats: Stats | null;
}

export default function SourceGrid({ stats }: Props) {
  const sources = stats?.sources ?? {};
  const entries = Object.entries(sources).sort((a, b) => b[1].file_count - a[1].file_count);

  if (entries.length === 0) {
    return (
      <section className="source-grid-section">
        <h2>Document Sources</h2>
        <p className="empty-hint">
          No documents downloaded yet. Run <code>make download</code> to populate the archive.
        </p>
      </section>
    );
  }

  return (
    <section className="source-grid-section">
      <h2>Document Sources</h2>
      <div className="source-grid">
        {entries.map(([key, info]) => (
          <Link key={key} to={`/sources/${key}`} className="source-card">
            <h3>{info.label}</h3>
            <p className="source-key">{key}</p>
            <div className="source-meta">
              <span>{info.file_count} files</span>
              <span>{info.total_size_mb} MB</span>
            </div>
            <div className="source-types">
              {Object.entries(info.file_types).map(([ext, count]) => (
                <span key={ext} className="type-badge">
                  {ext} ×{count}
                </span>
              ))}
            </div>
          </Link>
        ))}
      </div>
    </section>
  );
}
