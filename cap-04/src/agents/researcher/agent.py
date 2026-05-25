# src/agents/researcher/agent.py - versao cap-04
import asyncio
import os
from langchain_anthropic import ChatAnthropic
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from src.orchestrator.state import MarketIntelligenceState

llm = ChatAnthropic(model="claude-sonnet-4-6")

RESEARCHER_SYSTEM_PROMPT = """Voce e um especialista em pesquisa de mercado competitivo.
Sua tarefa: coletar dados sobre concorrentes, tendencias e posicionamento de mercado.

Use search_competitors para identificar os principais players de um mercado.
Use search_web para dados especificos sobre um player ou tendencia.
Use get_market_trends para capturar o que esta mudando no mercado.

Para cada pesquisa:
1. Identifique o mercado e a localizacao do pedido
2. Use search_competitors para listar os principais players
3. Use search_web para detalhar os 2-3 mais relevantes
4. Use get_market_trends para contexto de tendencias

Retorne JSON com:
- competitors: lista com name, differentiator, market_presence (alta/media/baixa)
- market_trends: lista de 3-5 tendencias identificadas
- data_sources: URLs consultadas"""

MCP_SERVER_CONFIG = {
    "research": {
        "url": os.getenv("RESEARCH_MCP_URL", "http://localhost:8001/mcp"),
        "transport": "http",
    }
}


async def researcher_node_async(state: MarketIntelligenceState) -> dict:
    """No pesquisador: conecta ao MCP server e executa pesquisa."""

    query = state["query"]

    async with MultiServerMCPClient(MCP_SERVER_CONFIG) as client:
        tools = client.get_tools()

        agent = create_react_agent(
            model=llm,
            tools=tools,
            state_modifier=RESEARCHER_SYSTEM_PROMPT,
        )

        result = await agent.ainvoke({
            "messages": [HumanMessage(content=f"Pesquise: {query}")]
        })

    research_result = result["messages"][-1].content

    return {
        "research_result": research_result,
        "messages": result["messages"],
    }


def researcher_node(state: MarketIntelligenceState) -> dict:
    """Wrapper sincrono para o no async - interface compativel com LangGraph."""
    return asyncio.run(researcher_node_async(state))
