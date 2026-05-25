# src/agents/analyzer/agent.py - versao cap-05 (sem alteracoes no cap-06)
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
- scored_competitors, market_gaps, recommended_positioning, analysis_confidence"""

MCP_SERVER_CONFIG = {
    "analysis": {
        "url": os.getenv("ANALYSIS_MCP_URL", "http://localhost:8002/mcp"),
        "transport": "http",
    }
}


async def analyzer_node_async(state: MarketIntelligenceState) -> dict:
    research_data = state.get("research_result", "")
    query = state.get("query", "")
    async with MultiServerMCPClient(MCP_SERVER_CONFIG) as client:
        tools = client.get_tools()
        agent = create_react_agent(model=llm, tools=tools, state_modifier=ANALYZER_SYSTEM_PROMPT)
        result = await agent.ainvoke({
            "messages": [HumanMessage(content=f"Analise estes dados para o mercado '{query}':\n\n{research_data}")]
        })
    return {"analysis_result": result["messages"][-1].content, "messages": result["messages"]}


def analyzer_node(state: MarketIntelligenceState) -> dict:
    return asyncio.run(analyzer_node_async(state))
