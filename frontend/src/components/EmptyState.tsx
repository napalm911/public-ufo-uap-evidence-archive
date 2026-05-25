import "./EmptyState.css";

interface Props {
  message: string;
  hint?: string;
}

export default function EmptyState({ message, hint }: Props) {
  return (
    <div className="empty-state">
      <p>{message}</p>
      {hint && <code>{hint}</code>}
    </div>
  );
}
