"""Human-readable labels for sources and topics."""

SOURCE_LABELS = {
    "aaro": "AARO Historical Reports",
    "blue_book": "Project Blue Book",
    "cia_crest": "CIA CREST Archive",
    "congress": "Congressional Hearings",
    "disclosure_act": "UAP Disclosure Act",
    "doe": "DOE / NNSA",
    "fbi": "FBI Vault",
    "foia": "FOIA Collections",
    "foreign": "Foreign Releases",
    "nasa": "NASA UAP Study",
    "navy_videos": "Navy UAP Videos",
    "odni": "ODNI Assessment",
    "pentagon": "Pentagon Briefings",
}

TOPIC_LABELS = {
    "hearing": "Congressional Hearings",
    "virginia_incidents": "Nimitz / Virginia Incidents",
    "roosevelt_incidents": "Roosevelt / Gimbal Incidents",
    "disclosure_legislation": "Disclosure Legislation",
    "nuclear_connections": "Nuclear Connections",
    "project_blue_book": "Project Blue Book",
    "cia_documents": "CIA Documents",
    "fbi_documents": "FBI Documents",
    "aaro_reports": "AARO Reports",
    "nasa_study": "NASA Study",
    "international": "International Releases",
}


def source_label(key: str) -> str:
    return SOURCE_LABELS.get(key, key.replace("_", " ").title())


def topic_label(key: str) -> str:
    return TOPIC_LABELS.get(key, key.replace("_", " ").title())
