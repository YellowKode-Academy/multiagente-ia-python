# src/agents/analyzer/mcp_server/server.py
from fastmcp import FastMCP
from .tools.scorer import score_competitor, score_competitors_batch
from .tools.gap_finder import identify_market_gaps, recommend_positioning

mcp = FastMCP(
    name="analysis-mcp-server",
    instructions="""Servidor MCP especializado em analise competitiva.

    Ferramentas disponiveis:
    - score_competitor: calcula score de ameaca de um unico concorrente
    - score_competitors_batch: processa lista completa de concorrentes (mais eficiente)
    - identify_market_gaps: identifica gaps nao cobertos pelos concorrentes
    - recommend_positioning: gera recomendacao de posicionamento

    Fluxo recomendado:
    1. score_competitors_batch com os concorrentes da pesquisa
    2. identify_market_gaps com a lista de concorrentes
    3. recommend_positioning com os resultados dos dois passos anteriores"""
)


@mcp.tool()
def score_competitor_tool(
    name: str,
    differentiator: str,
    market_presence: str,
    funding_stage: str = None,
    founded_year: int = None,
) -> str:
    """Calcula score de ameaca (0-100) de um concorrente especifico."""
    return score_competitor(name, differentiator, market_presence, funding_stage, founded_year)


@mcp.tool()
def score_competitors_batch_tool(competitors_json: str) -> str:
    """Processa lista de concorrentes e retorna todos os scores ordenados por ameaca."""
    return score_competitors_batch(competitors_json)


@mcp.tool()
def identify_market_gaps_tool(
    competitors_json: str,
    target_market: str,
    target_location: str = "Brasil",
) -> str:
    """Identifica gaps de mercado nao cobertos pelos concorrentes analisados."""
    return identify_market_gaps(competitors_json, target_market, target_location)


@mcp.tool()
def recommend_positioning_tool(
    scored_competitors_json: str,
    market_gaps_json: str,
) -> str:
    """Gera recomendacao de posicionamento baseada em scores e gaps."""
    return recommend_positioning(scored_competitors_json, market_gaps_json)


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8002)
