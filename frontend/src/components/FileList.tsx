import { useMemo, useState } from "react";
import { ArchiveFile } from "../types";
import FileRow from "./FileRow";
import EmptyState from "./EmptyState";
import "./FileList.css";

interface Props {
  files: ArchiveFile[];
  emptyMessage?: string;
}

type SortMode = "name" | "date";

export default function FileList({ files, emptyMessage = "No documents found." }: Props) {
  const [filter, setFilter] = useState("");
  const [sort, setSort] = useState<SortMode>("name");

  const filtered = useMemo(() => {
    let list = files;
    if (filter.trim()) {
      const q = filter.toLowerCase();
      list = list.filter(
        (f) => f.filename.toLowerCase().includes(q) || f.path.toLowerCase().includes(q)
      );
    }
    return [...list].sort((a, b) => {
      if (sort === "date") {
        const da = a.date || "";
        const db = b.date || "";
        if (da !== db) return db.localeCompare(da);
      }
      return a.filename.localeCompare(b.filename);
    });
  }, [files, filter, sort]);

  if (files.length === 0) {
    return <EmptyState message={emptyMessage} hint="make download" />;
  }

  return (
    <div className="file-list">
      <div className="file-list-controls">
        <input
          type="search"
          placeholder="Filter files…"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="file-filter"
        />
        <select value={sort} onChange={(e) => setSort(e.target.value as SortMode)} className="file-sort">
          <option value="name">Name A–Z</option>
          <option value="date">Date</option>
        </select>
      </div>
      <p className="file-count">{filtered.length} document{filtered.length !== 1 ? "s" : ""}</p>
      <div className="file-rows">
        {filtered.map((f) => (
          <FileRow key={f.id} file={f} />
        ))}
      </div>
      {filtered.length === 0 && filter && (
        <EmptyState message="No files match your filter." />
      )}
    </div>
  );
}
