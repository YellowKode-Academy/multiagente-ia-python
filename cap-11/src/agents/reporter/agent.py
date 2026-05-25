# src/agents/reporter/agent.py - versao cap-11
# Wrapper agora e async nativo
import os
from langchain_anthropic import ChatAnthropic
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from src.orchestrator.state import MarketIntelligenceState

llm = ChatAnthropic(model="claude-sonnet-4-6")

REPORTER_SYSTEM_PROMPT = "Especialista em relatorios. Use: generate_executive_summary, format_competitor_table, format_gaps_section, export_report."

MCP_SERVER_CONFIG = {
    "report": {
        "url": os.getenv("REPORT_MCP_URL", "http://localhost:8003/mcp"),
        "transport": "http",
    }
}


async def reporter_node_async(state: MarketIntelligenceState) -> dict:
    analysis_data = state.get("analysis_result", "")
    query = state.get("query", "analise de mercado")
    client = MultiServerMCPClient(MCP_SERVER_CONFIG)
    tools = await client.get_tools()
    agent = create_react_agent(model=llm, tools=tools, state_modifier=REPORTER_SYSTEM_PROMPT)
    result = await agent.ainvoke({"messages": [HumanMessage(content=f"Relatorio para: {query}\n\n{analysis_data}")]})
    return {"report": result["messages"][-1].content, "messages": result["messages"]}


async def reporter_node(state: MarketIntelligenceState) -> dict:
    return await reporter_node_async(state)
