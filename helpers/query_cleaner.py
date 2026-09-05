GENERIC_WORDS = {
    "donnees",
    "données",
    "fichier",
    "tableau",
    "csv",
    "excel",
    "xlsx",
    "json",
    "xml",
}


def clean_query(query: str) -> str:
    words = query.lower().split()
    cleaned_words = [w for w in words if w not in GENERIC_WORDS]
    return " ".join(cleaned_words) if cleaned_words else query
