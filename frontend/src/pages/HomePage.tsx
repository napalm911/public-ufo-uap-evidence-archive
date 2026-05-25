import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchStats } from "../api";
import { Stats } from "../types";
import Hero from "../components/Hero";
import SourceGrid from "../components/SourceGrid";
import EmptyState from "../components/EmptyState";
import { GridSkeleton } from "../components/Skeleton";
import "../components/SourceGrid.css";

export default function HomePage() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats()
      .then(setStats)
      .catch(() => setStats(null))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <>
        <Hero stats={null} />
        <GridSkeleton count={6} />
      </>
    );
  }

  return (
    <>
      <Hero stats={stats} />
      {stats && stats.total_files === 0 ? (
        <EmptyState
          message="No documents in the archive yet."
          hint="make download"
        />
      ) : (
        <>
          <SourceGrid stats={stats} />
          <section className="browse-shortcuts">
            <Link to="/timeline" className="shortcut-card">
              <h3>Timeline</h3>
              <p>Browse by date</p>
            </Link>
            <Link to="/topics" className="shortcut-card">
              <h3>Topics</h3>
              <p>Browse by theme</p>
            </Link>
          </section>
        </>
      )}
      <footer className="page-footer">
        <p>U.S. government public domain documents · MIT licensed tooling</p>
      </footer>
    </>
  );
}
