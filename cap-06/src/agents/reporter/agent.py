# src/agents/reporter/agent.py
import asyncio
import os
from langchain_anthropic import ChatAnthropic
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from src.orchestrator.state import MarketIntelligenceState

llm = ChatAnthropic(model="claude-sonnet-4-6")

REPORTER_SYSTEM_PROMPT = """Voce e um especialista em comunicacao de inteligencia competitiva.
Voce transforma dados de analise em relatorios profissionais em markdown.

Fluxo de trabalho obrigatorio:
1. generate_executive_summary com os dados de analise e a query original
2. format_competitor_table com os scored_competitors
3. format_gaps_section com os market_gaps
4. export_report combinando os tres resultados acima

Apos o export_report, retorne o path do arquivo gerado.
Nao invente dados. Use apenas as informacoes da analise recebida."""

MCP_SERVER_CONFIG = {
    "report": {
        "url": os.getenv("REPORT_MCP_URL", "http://localhost:8003/mcp"),
        "transport": "http",
    }
}


async def reporter_node_async(state: MarketIntelligenceState) -> dict:
    """No relator: gera o relatorio final a partir dos dados de analise."""

    analysis_data = state.get("analysis_result", "")
    query = state.get("query", "analise de mercado")

    async with MultiServerMCPClient(MCP_SERVER_CONFIG) as client:
        tools = client.get_tools()

        agent = create_react_agent(
            model=llm,
            tools=tools,
            state_modifier=REPORTER_SYSTEM_PROMPT,
        )

        result = await agent.ainvoke({
            "messages": [HumanMessage(
                content=f"""Gere o relatorio final para:

Query original: {query}

Dados de analise:
{analysis_data}"""
            )]
        })

    report = result["messages"][-1].content

    return {
        "report": report,
        "messages": result["messages"],
    }


def reporter_node(state: MarketIntelligenceState) -> dict:
    return asyncio.run(reporter_node_async(state))
