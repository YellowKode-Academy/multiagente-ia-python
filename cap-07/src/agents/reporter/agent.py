# src/agents/reporter/agent.py - versao cap-06 (sem alteracoes no cap-07)
import asyncio
import os
from langchain_anthropic import ChatAnthropic
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from src.orchestrator.state import MarketIntelligenceState

llm = ChatAnthropic(model="claude-sonnet-4-6")

REPORTER_SYSTEM_PROMPT = """Voce e um especialista em comunicacao de inteligencia competitiva.
Transforme os dados de analise em relatorio markdown profissional.

Fluxo obrigatorio:
1. generate_executive_summary
2. format_competitor_table
3. format_gaps_section
4. export_report

Nao invente dados. Use apenas as informacoes recebidas."""

MCP_SERVER_CONFIG = {
    "report": {
        "url": os.getenv("REPORT_MCP_URL", "http://localhost:8003/mcp"),
        "transport": "http",
    }
}


async def reporter_node_async(state: MarketIntelligenceState) -> dict:
    analysis_data = state.get("analysis_result", "")
    query = state.get("query", "analise de mercado")

    async with MultiServerMCPClient(MCP_SERVER_CONFIG) as client:
        tools = client.get_tools()
        agent = create_react_agent(model=llm, tools=tools, state_modifier=REPORTER_SYSTEM_PROMPT)
        result = await agent.ainvoke({
            "messages": [HumanMessage(content=f"Gere o relatorio para: {query}\n\nAnalise:\n{analysis_data}")]
        })

    return {"report": result["messages"][-1].content, "messages": result["messages"]}


def reporter_node(state: MarketIntelligenceState) -> dict:
    return asyncio.run(reporter_node_async(state))
