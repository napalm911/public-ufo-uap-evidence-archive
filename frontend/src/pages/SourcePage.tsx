import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchDocuments } from "../api";
import { ArchiveFile } from "../types";
import { sourceLabel } from "../lib/labels";
import Breadcrumbs from "../components/Breadcrumbs";
import PageHeader from "../components/PageHeader";
import FileList from "../components/FileList";
import { ListSkeleton } from "../components/Skeleton";
import "./pages.css";

export default function SourcePage() {
  const { sourceKey } = useParams<{ sourceKey: string }>();
  const [files, setFiles] = useState<ArchiveFile[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!sourceKey) return;
    setLoading(true);
    fetchDocuments({ source: sourceKey, limit: 500 })
      .then((data) => setFiles(data.files))
      .catch(() => setFiles([]))
      .finally(() => setLoading(false));
  }, [sourceKey]);

  const label = sourceKey ? sourceLabel(sourceKey) : "";

  return (
    <>
      <Breadcrumbs
        items={[
          { label: "Archive", to: "/" },
          { label: label || sourceKey || "" },
        ]}
      />
      <PageHeader
        title={label}
        subtitle={`${files.length} documents in this source`}
      />
      {loading ? <ListSkeleton rows={6} /> : <FileList files={files} />}
    </>
  );
}
