# src/agents/reporter/mcp_server/server.py
from fastmcp import FastMCP
from .tools.generator import (
    generate_executive_summary,
    format_competitor_table,
    format_gaps_section,
    export_report,
)

mcp = FastMCP(
    name="report-mcp-server",
    instructions="""Servidor MCP especializado em geracao de relatorios de inteligencia competitiva.

    Ferramentas disponiveis:
    - generate_executive_summary: gera o resumo executivo em markdown
    - format_competitor_table: formata tabela de concorrentes
    - format_gaps_section: formata secao de gaps de mercado
    - export_report: combina secoes e salva o relatorio final

    Fluxo obrigatorio:
    1. generate_executive_summary com analise + query original
    2. format_competitor_table com scored_competitors
    3. format_gaps_section com market_gaps
    4. export_report combinando os tres resultados"""
)


@mcp.tool()
def generate_executive_summary_tool(analysis_json: str, query: str) -> str:
    """Gera o resumo executivo do relatorio em markdown."""
    return generate_executive_summary(analysis_json, query)


@mcp.tool()
def format_competitor_table_tool(scored_competitors_json: str) -> str:
    """Formata tabela de concorrentes em markdown."""
    return format_competitor_table(scored_competitors_json)


@mcp.tool()
def format_gaps_section_tool(market_gaps_json: str) -> str:
    """Formata secao de gaps de mercado em markdown."""
    return format_gaps_section(market_gaps_json)


@mcp.tool()
def export_report_tool(
    executive_summary: str,
    competitor_table: str,
    gaps_section: str,
    output_path: str = "relatorio.md",
) -> str:
    """Combina secoes e exporta o relatorio final em markdown."""
    return export_report(executive_summary, competitor_table, gaps_section, output_path)


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8003)
