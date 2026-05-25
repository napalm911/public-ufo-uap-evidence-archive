import { useEffect, useState, useMemo } from "react";
import { Link } from "react-router-dom";
import { fetchTimeline } from "../api";
import { TimelineEntry } from "../types";
import Breadcrumbs from "../components/Breadcrumbs";
import PageHeader from "../components/PageHeader";
import EmptyState from "../components/EmptyState";
import { ListSkeleton } from "../components/Skeleton";
import { docUrl } from "../lib/docId";
import "./TimelinePage.css";

export default function TimelinePage() {
  const [entries, setEntries] = useState<TimelineEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTimeline()
      .then((data) => setEntries(data.entries))
      .catch(() => setEntries([]))
      .finally(() => setLoading(false));
  }, []);

  const byYear = useMemo(() => {
    const groups: Record<string, TimelineEntry[]> = {};
    for (const e of entries) {
      const year = e.date.slice(0, 4);
      if (!groups[year]) groups[year] = [];
      groups[year].push(e);
    }
    return Object.entries(groups).sort((a, b) => b[0].localeCompare(a[0]));
  }, [entries]);

  return (
    <>
      <Breadcrumbs items={[{ label: "Archive", to: "/" }, { label: "Timeline" }]} />
      <PageHeader title="Timeline" subtitle="Documents ordered by date inferred from filenames." />
      {loading ? (
        <ListSkeleton rows={8} />
      ) : entries.length === 0 ? (
        <EmptyState message="No dated entries yet." hint="make download" />
      ) : (
        <div className="timeline">
          {byYear.map(([year, items]) => (
            <section key={year} className="timeline-year">
              <h2 className="year-label">{year}</h2>
              <div className="timeline-entries">
                {items.map((e) => (
                  <Link key={e.file} to={docUrl(e.file)} className="timeline-entry">
                    <span className="timeline-dot" />
                    <span className="timeline-date">{e.date}</span>
                    <span className="timeline-name">{e.file.split("/").pop()}</span>
                    <span className="timeline-source">{e.source_label}</span>
                  </Link>
                ))}
              </div>
            </section>
          ))}
        </div>
      )}
    </>
  );
}
