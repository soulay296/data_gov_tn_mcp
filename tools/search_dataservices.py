import math

from config import settings
from helpers.api_client import DataGovError, datagov_client
from helpers.query_cleaner import clean_query


async def search_dataservices(
    query: str,
    page: int = 1,
    page_size: int = 20,
    organization: str | None = None,
    tags: list[str] | None = None,
) -> str:
    if not query or not query.strip():
        return "Veuillez fournir une requête de recherche."

    try:
        return await _search_dataservices(query, page, page_size, organization, tags)
    except DataGovError as exc:
        return str(exc)


async def _search_dataservices(
    query: str,
    page: int,
    page_size: int,
    organization: str | None,
    tags: list[str] | None,
) -> str:
    if page_size < 1:
        page_size = 20
    else:
        page_size = min(page_size, settings.MAX_PAGE_SIZE)
    page = max(1, page)

    cleaned = clean_query(query)
    start = (page - 1) * page_size

    fq_parts: list[str] = ["type:dataservice"]
    if organization:
        fq_parts.append(f"organization:{organization}")
    if tags:
        for tag in tags:
            fq_parts.append(f"tags:{tag}")
    fq = " AND ".join(fq_parts)

    async def _search(q: str) -> dict:
        params: dict = {"q": q, "rows": page_size, "start": start, "fq": fq}
        return await datagov_client.get("/action/package_search", params=params)

    data = await _search(cleaned)
    total = data["result"]["count"]
    results = data["result"]["results"]
    used_query = cleaned

    if total == 0 and cleaned != query:
        data = await _search(query)
        total = data["result"]["count"]
        results = data["result"]["results"]
        used_query = query

    if total == 0:
        words = cleaned.split()
        for i in range(len(words) - 1, 0, -1):
            reduced = " ".join(words[:i])
            data = await _search(reduced)
            total = data["result"]["count"]
            results = data["result"]["results"]
            used_query = reduced
            if total > 0:
                break

    if total == 0:
        return f"Aucun dataservice trouvé pour '{query}'."

    total_pages = math.ceil(total / page_size)

    lines: list[str] = []
    lines.append(f"{total} dataservice(s) trouvé(s) pour '{query}' :")
    lines.append(f"Page {page}/{total_pages} ({page_size} par page)")
    lines.append("")

    if used_query != query:
        lines.append(f"Recherche élargie : requête réduite à '{used_query}'")
        lines.append("")

    for i, service in enumerate(results, start=1):
        titre = service.get("title", "Sans titre")
        service_id = service.get("id", "")
        description = (service.get("notes") or "").strip()
        organisation = (service.get("organization") or {}).get(
            "title", "Organisation inconnue"
        )
        base_url = service.get("url", "Non renseignée")
        modified = service.get("metadata_modified", "")
        service_tags = [t.get("name", "") for t in (service.get("tags") or [])]

        lines.append(f"{i}. {titre}")
        lines.append(f"   ID : {service_id}")
        lines.append(f"   Organisation : {organisation}")
        lines.append(f"   URL de base : {base_url}")
        if description:
            if len(description) > 150:
                description = description[:147] + "..."
            lines.append(f"   Description : {description}")
        if service_tags:
            lines.append(f"   Tags : {', '.join(service_tags)}")
        if modified:
            lines.append(f"   Modified : {modified}")
        lines.append("")

    return "\n".join(lines)
