import { Stats } from "../types";
import "./Hero.css";

interface Props {
  stats: Stats | null;
}

export default function Hero({ stats }: Props) {
  return (
    <header className="hero">
      <p className="hero-eyebrow">Declassified · FOIA · Official Records</p>
      <h1 className="hero-title">
        Public UFO / UAP
        <br />
        <em>Evidence Archive</em>
      </h1>
      <p className="hero-tagline">
        Search and analyze U.S. government documents on unidentified anomalous phenomena
        using semantic vector search and AI-assisted research.
      </p>
      <div className="hero-stats">
        <div className="stat">
          <span className="stat-value">{stats?.total_sources ?? "—"}</span>
          <span className="stat-label">Sources</span>
        </div>
        <div className="stat">
          <span className="stat-value">{stats?.total_files ?? "—"}</span>
          <span className="stat-label">Documents</span>
        </div>
        <div className="stat">
          <span className="stat-value">{stats?.indexed_chunks ?? "—"}</span>
          <span className="stat-label">Indexed Chunks</span>
        </div>
      </div>
    </header>
  );
}
