# src/agents/researcher/mcp_server/server.py
# (identico ao cap-04 - copiado para manter cap-05 autocontido)
from dotenv import load_dotenv
load_dotenv()

from fastmcp import FastMCP
from .tools.web_search import search_web, search_competitors

mcp = FastMCP(name="research-mcp-server")


@mcp.tool()
async def search_web_tool(query: str, max_results: int = 5) -> str:
    """Busca informacoes na web."""
    return await search_web(query, max_results)


@mcp.tool()
async def search_competitors_tool(market: str, location: str = "Brasil") -> str:
    """Busca concorrentes em um mercado especifico."""
    return await search_competitors(market, location)


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8001)
