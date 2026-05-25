# src/agents/analyzer/agent.py - versao cap-05
import asyncio
import os
from langchain_anthropic import ChatAnthropic
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from src.orchestrator.state import MarketIntelligenceState

llm = ChatAnthropic(model="claude-sonnet-4-6")

ANALYZER_SYSTEM_PROMPT = """Voce e um analista de inteligencia competitiva.
Voce recebe dados de pesquisa e produz analise estruturada usando as ferramentas disponiveis.

Fluxo de trabalho obrigatorio:
1. Use score_competitors_batch com os concorrentes da pesquisa
2. Use identify_market_gaps com a lista de concorrentes e o mercado alvo
3. Use recommend_positioning com os resultados dos passos 1 e 2

Retorne APENAS o JSON final com:
- scored_competitors: resultado do score_competitors_batch
- market_gaps: resultado do identify_market_gaps
- recommended_positioning: resultado do recommend_positioning
- analysis_confidence: numero 0-1"""

MCP_SERVER_CONFIG = {
    "analysis": {
        "url": os.getenv("ANALYSIS_MCP_URL", "http://localhost:8002/mcp"),
        "transport": "http",
    }
}


async def analyzer_node_async(state: MarketIntelligenceState) -> dict:
    """No analisador: conecta ao MCP server e executa analise."""

    research_data = state.get("research_result", "")
    query = state.get("query", "")

    client = MultiServerMCPClient(MCP_SERVER_CONFIG)
    tools = await client.get_tools()

    agent = create_react_agent(
        model=llm,
        tools=tools,
        state_modifier=ANALYZER_SYSTEM_PROMPT,
    )

    result = await agent.ainvoke({
        "messages": [HumanMessage(
            content=f"Analise estes dados de pesquisa para o mercado '{query}':\n\n{research_data}"
        )]
    })

    analysis_result = result["messages"][-1].content

    return {
        "analysis_result": analysis_result,
        "messages": result["messages"],
    }


def analyzer_node(state: MarketIntelligenceState) -> dict:
    return asyncio.run(analyzer_node_async(state))
