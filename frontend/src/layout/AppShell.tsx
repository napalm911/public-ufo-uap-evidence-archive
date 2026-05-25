import { Link, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import { fetchHealth } from "../api";
import "./AppShell.css";

interface Props {
  children: React.ReactNode;
}

const MAIN_NAV = [
  { to: "/", label: "Browse", match: (p: string) => p === "/" || p.startsWith("/sources") || p.startsWith("/documents") },
  { to: "/ask", label: "Ask", match: (p: string) => p.startsWith("/ask") },
  { to: "/search", label: "Search", match: (p: string) => p.startsWith("/search") },
];

const SECONDARY_NAV = [
  { to: "/timeline", label: "Timeline" },
  { to: "/topics", label: "Topics" },
];

export default function AppShell({ children }: Props) {
  const location = useLocation();
  const [indexedChunks, setIndexedChunks] = useState<number | null>(null);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    fetchHealth()
      .then((h) => setIndexedChunks(h.indexed_chunks))
      .catch(() => setIndexedChunks(null));
  }, []);

  const path = location.pathname;

  return (
    <div className="app-shell">
      <header className="top-bar">
        <Link to="/" className="brand">
          <span className="brand-title">UAP Evidence Archive</span>
        </Link>
        {indexedChunks != null && (
          <span className="index-pill">{indexedChunks} indexed</span>
        )}
        <button
          className="menu-toggle"
          onClick={() => setMenuOpen(!menuOpen)}
          aria-label="Menu"
        >
          ☰
        </button>
      </header>

      <div className="shell-body">
        <aside className={`sidebar ${menuOpen ? "open" : ""}`}>
          <nav className="sidebar-nav">
            {MAIN_NAV.map((item) => (
              <Link
                key={item.to}
                to={item.to}
                className={`nav-link ${item.match(path) ? "active" : ""}`}
                onClick={() => setMenuOpen(false)}
              >
                {item.label}
              </Link>
            ))}
            <div className="nav-divider" />
            {SECONDARY_NAV.map((item) => (
              <Link
                key={item.to}
                to={item.to}
                className={`nav-link secondary ${path.startsWith(item.to) ? "active" : ""}`}
                onClick={() => setMenuOpen(false)}
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </aside>

        <main className="main-content">{children}</main>
      </div>

      <nav className="bottom-nav">
        {MAIN_NAV.map((item) => (
          <Link
            key={item.to}
            to={item.to}
            className={`bottom-link ${item.match(path) ? "active" : ""}`}
          >
            {item.label}
          </Link>
        ))}
      </nav>
    </div>
  );
}
