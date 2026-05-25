export function encodeDocId(path: string): string {
  return encodeURIComponent(path);
}

export function decodeDocId(docId: string): string {
  return decodeURIComponent(docId);
}

export function docPathFromCitation(source: string, filename: string): string {
  return `data/${source}/${filename}`;
}

export function docUrl(path: string): string {
  return `/documents/${encodeDocId(path)}`;
}

export function fileDownloadUrl(path: string): string {
  // path is data/source/file.pdf -> /files/source/file.pdf
  const rel = path.startsWith("data/") ? path.slice(5) : path;
  return `/files/${rel}`;
}
