from unittest.mock import AsyncMock, patch

from tools.search_dataservices import search_dataservices


def _service(title: str, service_id: str, url: str) -> dict:
    return {
        "title": title,
        "id": service_id,
        "notes": "",
        "url": url,
        "organization": {"title": "Org Test"},
        "tags": [{"name": "api"}],
    }


def _search_response(count: int, results: list[dict]) -> dict:
    return {"success": True, "result": {"count": count, "results": results}}


async def test_search_dataservices_empty_query() -> None:
    assert (
        await search_dataservices("  ") == "Veuillez fournir une requête de recherche."
    )


async def test_search_dataservices_forces_type_dataservice() -> None:
    mock = AsyncMock(
        return_value=_search_response(1, [_service("API Carte", "s1", "http://x")])
    )
    with patch("tools.search_dataservices.datagov_client.get", mock) as m:
        await search_dataservices("carte")
    params = m.await_args.kwargs["params"]
    assert params["fq"] == "type:dataservice"


async def test_search_dataservices_returns_formatted_results() -> None:
    mock = AsyncMock(
        return_value=_search_response(1, [_service("API Carte", "s1", "https://x.com")])
    )
    with patch("tools.search_dataservices.datagov_client.get", mock):
        result = await search_dataservices("carte")
    assert "1 dataservice(s) trouvé(s)" in result
    assert "API Carte" in result
    assert "https://x.com" in result


async def test_search_dataservices_no_results() -> None:
    mock = AsyncMock(return_value=_search_response(0, []))
    with patch("tools.search_dataservices.datagov_client.get", mock):
        result = await search_dataservices("zzz")
    assert "Aucun dataservice trouvé" in result


async def test_search_dataservices_api_error_returns_message() -> None:
    from helpers.api_client import DataGovError

    mock = AsyncMock(side_effect=DataGovError("boom"))
    with patch("tools.search_dataservices.datagov_client.get", mock):
        result = await search_dataservices("carte")
    assert "boom" in result
