import { Link } from "react-router-dom";
import { TopicInfo } from "../types";
import "./TopicCard.css";

interface Props {
  topic: TopicInfo;
}

export default function TopicCard({ topic }: Props) {
  return (
    <Link to={`/topics/${topic.key}`} className="topic-card">
      <h3>{topic.label}</h3>
      <p className="topic-count">{topic.count} document{topic.count !== 1 ? "s" : ""}</p>
    </Link>
  );
}
