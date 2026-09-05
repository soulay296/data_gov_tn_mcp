from unittest.mock import AsyncMock, patch

from tools.search_datasets import search_datasets


def _dataset(title: str, dataset_id: str, description: str = "") -> dict:
    return {
        "title": title,
        "id": dataset_id,
        "notes": description,
        "organization": {"title": "Org Test"},
        "num_resources": 1,
        "metadata_modified": "2023-01-01T00:00:00.000000",
        "tags": [{"name": "tag1"}, {"name": "tag2"}],
    }


def _search_response(count: int, results: list[dict]) -> dict:
    return {"success": True, "result": {"count": count, "results": results}}


async def test_search_datasets_empty_query() -> None:
    assert await search_datasets("   ") == "Veuillez fournir une requête de recherche."


async def test_search_datasets_returns_formatted_results() -> None:
    mock = AsyncMock(
        return_value=_search_response(1, [_dataset("Population", "id1", "desc")])
    )
    with patch("tools.search_datasets.datagov_client.get", mock):
        result = await search_datasets("population")
    assert "1 résultat(s) trouvé(s)" in result
    assert "Population" in result
    assert "Page 1/1" in result


async def test_search_datasets_empty_query_skips_api() -> None:
    with patch("tools.search_datasets.datagov_client.get", AsyncMock()) as mock:
        await search_datasets("")
    mock.assert_not_awaited()


async def test_search_datasets_no_results() -> None:
    mock = AsyncMock(return_value=_search_response(0, []))
    with patch("tools.search_datasets.datagov_client.get", mock):
        result = await search_datasets("zzzzyx")
    assert "Aucun résultat trouvé" in result


async def test_search_datasets_falls_back_to_reduced_query() -> None:
    calls: list[str] = []

    def side_effect(path, params=None):
        q = params.get("q")
        calls.append(q)
        if q == "population recensement":
            return _search_response(0, [])
        return _search_response(
            2, [_dataset("Recensement", "a"), _dataset("Recensement 2", "b")]
        )

    mock = AsyncMock(side_effect=side_effect)
    with patch("tools.search_datasets.datagov_client.get", mock):
        result = await search_datasets("population recensement")
    assert "Recherche élargie" in result
    assert "2 résultat(s)" in result
    assert "population recensement" in calls
    assert "population" in calls


async def test_search_datasets_filters_organization_and_tags() -> None:
    mock = AsyncMock(return_value=_search_response(1, [_dataset("D", "d")]))
    with patch("tools.search_datasets.datagov_client.get", mock) as m:
        await search_datasets("population", organization="ins", tags=["eau"])
    params = m.await_args.kwargs["params"]
    assert params["fq"] == "organization:ins AND tags:eau"


async def test_search_datasets_api_error_returns_message() -> None:
    from helpers.api_client import DataGovError

    mock = AsyncMock(side_effect=DataGovError("boom"))
    with patch("tools.search_datasets.datagov_client.get", mock):
        result = await search_datasets("population")
    assert "boom" in result
