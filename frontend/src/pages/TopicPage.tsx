import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchDocuments } from "../api";
import { ArchiveFile } from "../types";
import { topicLabel } from "../lib/labels";
import Breadcrumbs from "../components/Breadcrumbs";
import PageHeader from "../components/PageHeader";
import FileList from "../components/FileList";
import { ListSkeleton } from "../components/Skeleton";

export default function TopicPage() {
  const { topicKey } = useParams<{ topicKey: string }>();
  const [files, setFiles] = useState<ArchiveFile[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!topicKey) return;
    setLoading(true);
    fetchDocuments({ topic: topicKey, limit: 500 })
      .then((data) => setFiles(data.files))
      .catch(() => setFiles([]))
      .finally(() => setLoading(false));
  }, [topicKey]);

  const label = topicKey ? topicLabel(topicKey) : "";

  return (
    <>
      <Breadcrumbs
        items={[
          { label: "Archive", to: "/" },
          { label: "Topics", to: "/topics" },
          { label: label || topicKey || "" },
        ]}
      />
      <PageHeader title={label} subtitle={`${files.length} tagged documents`} />
      {loading ? <ListSkeleton rows={6} /> : <FileList files={files} />}
    </>
  );
}
