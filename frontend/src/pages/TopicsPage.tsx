import { useEffect, useState } from "react";
import { fetchTopics } from "../api";
import { TopicInfo } from "../types";
import Breadcrumbs from "../components/Breadcrumbs";
import PageHeader from "../components/PageHeader";
import TopicCard from "../components/TopicCard";
import EmptyState from "../components/EmptyState";
import { GridSkeleton } from "../components/Skeleton";
import "../components/TopicCard.css";

export default function TopicsPage() {
  const [topics, setTopics] = useState<TopicInfo[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTopics()
      .then((data) => setTopics(data.topics))
      .catch(() => setTopics([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <>
      <Breadcrumbs items={[{ label: "Archive", to: "/" }, { label: "Topics" }]} />
      <PageHeader title="Topics" subtitle="Browse documents by thematic category." />
      {loading ? (
        <GridSkeleton count={6} />
      ) : topics.length === 0 ? (
        <EmptyState message="No tagged documents yet." hint="make download" />
      ) : (
        <div className="topic-grid">
          {topics.map((t) => (
            <TopicCard key={t.key} topic={t} />
          ))}
        </div>
      )}
    </>
  );
}
