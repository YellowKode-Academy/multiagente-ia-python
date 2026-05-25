# tests/integration/test_researcher.py
import pytest
import json
from unittest.mock import patch, AsyncMock, MagicMock
from langchain_core.messages import AIMessage


@pytest.mark.asyncio
async def test_researcher_returns_structured_data():
    """Researcher deve retornar research_result estruturado."""
    mock_result_content = json.dumps({
        "competitors": [
            {"name": "Salesforce", "differentiator": "enterprise CRM", "market_presence": "alta"},
            {"name": "Pipedrive", "differentiator": "sales pipeline", "market_presence": "media"},
        ],
        "market_trends": ["crescimento de 18% ao ano", "adocao por PMEs"],
        "data_sources": ["IDC Brasil 2025", "Gartner Magic Quadrant"]
    })

    mock_agent_result = {
        "messages": [AIMessage(content=mock_result_content)]
    }

    mock_tools = [MagicMock(name="search_competitors_tool")]

    state = {
        "query": "analise CRM Brasil",
        "research_result": None,
        "analysis_result": None,
        "report": None,
        "next": "",
        "phase": "",
        "messages": [],
        "completed_agents": [],
    }

    mock_client = AsyncMock()
    mock_client.get_tools = AsyncMock(return_value=mock_tools)

    mock_agent = MagicMock()
    mock_agent.ainvoke = AsyncMock(return_value=mock_agent_result)

    with patch("src.agents.researcher.agent.MultiServerMCPClient", return_value=mock_client), \
         patch("src.agents.researcher.agent.create_react_agent", return_value=mock_agent):
        from src.agents.researcher.agent import researcher_node_async
        result = await researcher_node_async(state)

    assert "research_result" in result
    assert isinstance(result["research_result"], str)
    assert len(result["research_result"]) > 0
    assert "messages" in result
    assert isinstance(result["messages"], list)
