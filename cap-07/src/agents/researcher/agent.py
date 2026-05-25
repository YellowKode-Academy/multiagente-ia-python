# src/agents/researcher/agent.py - versao cap-07
# O researcher_node agora recebe apenas {"query": ...} via Send()
import asyncio
import os
from langchain_anthropic import ChatAnthropic
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

llm = ChatAnthropic(model="claude-sonnet-4-6")

RESEARCHER_SYSTEM_PROMPT = """Voce e um especialista em pesquisa de mercado competitivo.
Coleta dados sobre concorrentes, tendencias e posicionamento de mercado.

Use search_competitors para os principais players.
Use search_web para detalhes especificos.

Retorne JSON com: competitors, market_trends, data_sources."""

MCP_SERVER_CONFIG = {
    "research": {
        "url": os.getenv("RESEARCH_MCP_URL", "http://localhost:8001/mcp"),
        "transport": "http",
    }
}


async def researcher_node_async(state: dict) -> dict:
    """No pesquisador: conecta ao MCP server e executa pesquisa."""
    query = state["query"]

    async with MultiServerMCPClient(MCP_SERVER_CONFIG) as client:
        tools = client.get_tools()
        agent = create_react_agent(model=llm, tools=tools, state_modifier=RESEARCHER_SYSTEM_PROMPT)
        result = await agent.ainvoke({"messages": [HumanMessage(content=f"Pesquise: {query}")]})

    return {
        "research_result": result["messages"][-1].content,
        "messages": result["messages"],
        "completed_agents": ["researcher"],
    }


def researcher_node(state: dict) -> dict:
    """Wrapper sincrono - compativel com Send() que passa estado parcial."""
    return asyncio.run(researcher_node_async(state))
