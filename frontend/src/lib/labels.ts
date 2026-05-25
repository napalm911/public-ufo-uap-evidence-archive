export const SOURCE_LABELS: Record<string, string> = {
  aaro: "AARO Historical Reports",
  blue_book: "Project Blue Book",
  cia_crest: "CIA CREST Archive",
  congress: "Congressional Hearings",
  disclosure_act: "UAP Disclosure Act",
  doe: "DOE / NNSA",
  fbi: "FBI Vault",
  foia: "FOIA Collections",
  foreign: "Foreign Releases",
  nasa: "NASA UAP Study",
  navy_videos: "Navy UAP Videos",
  odni: "ODNI Assessment",
  pentagon: "Pentagon Briefings",
};

export const TOPIC_LABELS: Record<string, string> = {
  hearing: "Congressional Hearings",
  virginia_incidents: "Nimitz / Virginia Incidents",
  roosevelt_incidents: "Roosevelt / Gimbal Incidents",
  disclosure_legislation: "Disclosure Legislation",
  nuclear_connections: "Nuclear Connections",
  project_blue_book: "Project Blue Book",
  cia_documents: "CIA Documents",
  fbi_documents: "FBI Documents",
  aaro_reports: "AARO Reports",
  nasa_study: "NASA Study",
  international: "International Releases",
};

export function sourceLabel(key: string): string {
  return SOURCE_LABELS[key] ?? key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

export function topicLabel(key: string): string {
  return TOPIC_LABELS[key] ?? key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}
