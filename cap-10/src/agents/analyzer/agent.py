# src/agents/analyzer/agent.py - versao cap-07
import asyncio
import os
from langchain_anthropic import ChatAnthropic
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

llm = ChatAnthropic(model="claude-sonnet-4-6")
ANALYZER_SYSTEM_PROMPT = "Analista competitivo. Use score_competitors_batch, identify_market_gaps, recommend_positioning. Retorne JSON."
MCP_SERVER_CONFIG = {"analysis": {"url": os.getenv("ANALYSIS_MCP_URL", "http://localhost:8002/mcp"), "transport": "http"}}


async def analyzer_node_async(state: dict) -> dict:
    query = state.get("query", "")
    research_data = state.get("research_result", "")
    client = MultiServerMCPClient(MCP_SERVER_CONFIG)
    tools = await client.get_tools()
    agent = create_react_agent(model=llm, tools=tools, state_modifier=ANALYZER_SYSTEM_PROMPT)
    result = await agent.ainvoke({"messages": [HumanMessage(content=f"Analise '{query}'.\n\n{research_data}")]})
    return {"analysis_result": result["messages"][-1].content, "messages": result["messages"], "completed_agents": ["analyzer"]}


def analyzer_node(state: dict) -> dict:
    return asyncio.run(analyzer_node_async(state))
