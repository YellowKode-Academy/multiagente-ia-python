# src/agents/analyzer/agent.py - versao cap-07
# O analyzer_node agora recebe apenas {"query": ...} via Send()
import asyncio
import os
from langchain_anthropic import ChatAnthropic
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

llm = ChatAnthropic(model="claude-sonnet-4-6")

ANALYZER_SYSTEM_PROMPT = """Voce e um analista de inteligencia competitiva.
Quando receber dados de pesquisa, use as ferramentas para:
1. score_competitors_batch com os concorrentes
2. identify_market_gaps com os concorrentes e mercado
3. recommend_positioning com os resultados anteriores

Retorne JSON com: scored_competitors, market_gaps, recommended_positioning, analysis_confidence."""

MCP_SERVER_CONFIG = {
    "analysis": {
        "url": os.getenv("ANALYSIS_MCP_URL", "http://localhost:8002/mcp"),
        "transport": "http",
    }
}


async def analyzer_node_async(state: dict) -> dict:
    """No analisador: conecta ao MCP server e executa analise."""
    query = state.get("query", "")
    research_data = state.get("research_result", "Dados de pesquisa ainda nao disponiveis - use o mercado da query para analise.")

    client = MultiServerMCPClient(MCP_SERVER_CONFIG)
    tools = await client.get_tools()
    agent = create_react_agent(model=llm, tools=tools, state_modifier=ANALYZER_SYSTEM_PROMPT)
    result = await agent.ainvoke({
        "messages": [HumanMessage(content=f"Analise o mercado '{query}'.\n\nDados: {research_data}")]
    })

    return {
        "analysis_result": result["messages"][-1].content,
        "messages": result["messages"],
        "completed_agents": ["analyzer"],
    }


def analyzer_node(state: dict) -> dict:
    """Wrapper sincrono - compativel com Send() que passa estado parcial."""
    return asyncio.run(analyzer_node_async(state))
