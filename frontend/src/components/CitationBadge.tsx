import { Link } from "react-router-dom";
import { SearchResult } from "../types";
import { docPathFromCitation, docUrl } from "../lib/docId";
import "./CitationBadge.css";

interface Props {
  source: SearchResult;
  index: number;
}

export default function CitationBadge({ source, index }: Props) {
  const docPath = docPathFromCitation(source.source, source.filename);

  return (
    <details className="citation">
      <summary>
        [{index}]{" "}
        <Link to={docUrl(docPath)} className="citation-link" onClick={(e) => e.stopPropagation()}>
          {source.filename}
        </Link>
        <span className="citation-score">{(source.score * 100).toFixed(0)}%</span>
      </summary>
      <p className="citation-meta">
        Source: <strong>{source.source}</strong>
        {source.topics && <> · Topics: {source.topics}</>}
      </p>
      <p className="citation-text">
        {source.text.slice(0, 400)}
        {source.text.length > 400 ? "…" : ""}
      </p>
    </details>
  );
}
