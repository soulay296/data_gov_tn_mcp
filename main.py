from datetime import UTC, datetime

from fastmcp import FastMCP
from starlette.responses import JSONResponse

from config import settings
from logging_config import setup_logging
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
