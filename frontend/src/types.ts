export interface SourceInfo {
  label: string;
  file_count: number;
  total_size_mb: number;
  file_types: Record<string, number>;
}

export interface Stats {
  total_files: number;
  total_sources: number;
  generated: string | null;
  indexed_chunks: number;
  sources: Record<string, SourceInfo>;
}

export interface ArchiveFile {
  id: string;
  path: string;
  filename: string;
  source: string;
  source_label: string;
  extension: string;
  size_bytes: number;
  modified: string;
  topics: string[];
  topic_labels: string[];
  date: string | null;
}

export interface DocumentListResponse {
  total: number;
  limit: number;
  offset: number;
  files: ArchiveFile[];
}

export interface TimelineEntry {
  date: string;
  file: string;
  source: string;
  source_label: string;
}

export interface TimelineResponse {
  total_dated_entries: number;
  entries: TimelineEntry[];
}

export interface TopicInfo {
  key: string;
  label: string;
  count: number;
}

export interface TopicsResponse {
  topics: TopicInfo[];
}

export interface DocumentTextResponse {
  id: string;
  path: string;
  text: string;
}

export interface SearchResult {
  text: string;
  source: string;
  filename: string;
  chunk_index: number;
  topics: string;
  score: number;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  sources?: SearchResult[];
}

export interface BreadcrumbItem {
  label: string;
  to?: string;
}
