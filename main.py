from datetime import UTC, datetime

from fastmcp import FastMCP
from starlette.responses import JSONResponse

from config import settings
from logging_config import setup_logging
from tools.get_dataservice_info import get_dataservice_info as _get_dataservice_info
from tools.get_dataservice_openapi_spec import (
    get_dataservice_openapi_spec as _get_dataservice_openapi_spec,
)
from tools.get_dataset_info import get_dataset_info as _get_dataset_info
from tools.get_resource_info import get_resource_info as _get_resource_info
from tools.list_dataset_resources import (
    list_dataset_resources as _list_dataset_resources,
)
from tools.search_dataservices import search_dataservices as _search_dataservices
from tools.search_datasets import search_datasets as _search_datasets

setup_logging()

mcp = FastMCP("data.gov.tn-mcp")


@mcp.tool()
async def search_datasets(
    query: str,
    page: int = 1,
    page_size: int = 20,
    organization: str | None = None,
    tags: list[str] | None = None,
) -> str:
    """Rechercher des jeux de données par mots-clés."""
    return await _search_datasets(query, page, page_size, organization, tags)


@mcp.tool()
async def search_dataservices(
    query: str,
    page: int = 1,
    page_size: int = 20,
    organization: str | None = None,
    tags: list[str] | None = None,
) -> str:
    """Rechercher des dataservices (APIs externes référencées)."""
    return await _search_dataservices(query, page, page_size, organization, tags)


@mcp.tool()
async def get_dataset_info(dataset_id: str, lang: str = "fr") -> str:
    """Récupérer les métadonnées détaillées d'un jeu de données (fr, ar, en)."""
    return await _get_dataset_info(dataset_id, lang)


@mcp.tool()
async def list_dataset_resources(
    dataset_id: str, page: int = 1, page_size: int = 20, lang: str = "fr"
) -> str:
    """Lister les ressources (fichiers) attachées à un dataset (fr, ar, en)."""
    return await _list_dataset_resources(dataset_id, page, page_size, lang)


@mcp.tool()
async def get_resource_info(resource_id: str, lang: str = "fr") -> str:
    """Récupérer les métadonnées détaillées d'une ressource (fr, ar, en)."""
    return await _get_resource_info(resource_id, lang)


@mcp.tool()
async def get_dataservice_info(dataservice_id: str, lang: str = "fr") -> str:
    """Récupérer les métadonnées d'un dataservice (fr, ar, en)."""
    return await _get_dataservice_info(dataservice_id, lang)


@mcp.tool()
async def get_dataservice_openapi_spec(dataservice_id: str, lang: str = "fr") -> str:
    """Récupérer la spécification OpenAPI d'un dataservice (fr, ar, en)."""
    return await _get_dataservice_openapi_spec(dataservice_id, lang)


START_TIME = datetime.now(UTC)


async def health(request):
    return JSONResponse(
        {
            "status": "healthy",
            "uptime_since": START_TIME.isoformat(),
            "version": "1.0.0",
            "env": settings.MCP_ENV,
            "data_env": settings.DATAGOV_API_ENV,
            "timestamp": datetime.now(UTC).isoformat(),
        }
    )


@mcp.custom_route("/health", methods=["GET"])
async def health_route(request):
    return await health(request)


if __name__ == "__main__":
    mcp.run(transport="http", host=settings.MCP_HOST, port=settings.MCP_PORT)
