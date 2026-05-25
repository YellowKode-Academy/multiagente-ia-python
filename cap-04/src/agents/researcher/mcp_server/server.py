# src/agents/researcher/mcp_server/server.py
from dotenv import load_dotenv
load_dotenv()

from fastmcp import FastMCP
from .tools.web_search import search_web, search_competitors
from .tools.trends import get_market_trends

# Criar o servidor MCP
mcp = FastMCP(
    name="research-mcp-server",
    instructions="""Servidor MCP especializado em pesquisa de mercado competitivo.

    Ferramentas disponiveis:
    - search_web: busca informacoes gerais na web
    - search_competitors: busca especifica de concorrentes em um mercado
    - get_market_trends: identifica tendencias recentes

    Use search_competitors para buscas de concorrentes (mais eficiente que search_web generico).
    Use search_web para informacoes especificas sobre um player ou tecnologia."""
)


# Registrar ferramentas como MCP tools
@mcp.tool()
async def search_web_tool(query: str, max_results: int = 5) -> str:
    """Busca informacoes na web. Use para pesquisa geral ou dados de um player especifico."""
    return await search_web(query, max_results)


@mcp.tool()
async def search_competitors_tool(market: str, location: str = "Brasil") -> str:
    """Busca concorrentes em um mercado especifico. Mais eficiente que search_web para este fim."""
    return await search_competitors(market, location)


@mcp.tool()
async def get_market_trends_tool(market: str, timeframe: str = "6 months") -> str:
    """Identifica tendencias recentes em um mercado."""
    return await get_market_trends(market, timeframe)


if __name__ == "__main__":
    # Rodar o servidor em modo HTTP (para desenvolvimento e producao)
    mcp.run(transport="http", host="0.0.0.0", port=8001)
