from datetime import datetime, timezone

from starlette.responses import JSONResponse
from fastmcp import FastMCP

from config import settings
from logging_config import setup_logging

setup_logging()

mcp = FastMCP("data.gov.tn-mcp")

START_TIME = datetime.now(timezone.utc)


async def health(request):
    return JSONResponse({
        "status": "healthy",
        "uptime_since": START_TIME.isoformat(),
        "version": "1.0.0",
        "env": settings.MCP_ENV,
        "data_env": settings.DATAGOV_API_ENV,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


@mcp.custom_route("/health", methods=["GET"])
async def health_route(request):
    return await health(request)


if __name__ == "__main__":
    mcp.run(transport="http", host=settings.MCP_HOST, port=settings.MCP_PORT)
    