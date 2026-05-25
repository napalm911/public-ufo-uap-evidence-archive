import { Link } from "react-router-dom";
import { ArchiveFile } from "../types";
import { formatBytes } from "../lib/format";
import { docUrl } from "../lib/docId";
import { topicLabel } from "../lib/labels";
import "./FileRow.css";

interface Props {
  file: ArchiveFile;
}

function typeClass(ext: string): string {
  if (ext === ".pdf") return "type-pdf";
  if (ext === ".html") return "type-html";
  if (ext === ".mp4") return "type-video";
  return "type-default";
}

export default function FileRow({ file }: Props) {
  return (
    <Link to={docUrl(file.path)} className="file-row">
      <div className="file-main">
        <span className="file-name">{file.filename}</span>
        <span className="file-meta">
          <span className={`type-badge ${typeClass(file.extension)}`}>{file.extension || "file"}</span>
          {file.size_bytes > 0 && <span>{formatBytes(file.size_bytes)}</span>}
          {file.date && <span>{file.date}</span>}
        </span>
      </div>
      {file.topics.length > 0 && (
        <div className="file-topics">
          {file.topics.map((t) => (
            <span key={t} className="topic-pill">{topicLabel(t)}</span>
          ))}
        </div>
      )}
    </Link>
  );
}
