# tests/integration/test_researcher.py
import pytest
import json
import respx
import httpx
from src.agents.researcher.agent import researcher_node_async


@pytest.fixture
def mock_research_mcp():
    """Mocka o research-mcp-server para retornar dados fixos."""
    tools_response = {
        "tools": [
            {
                "name": "search_competitors_tool",
                "description": "Busca concorrentes em um mercado",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "market": {"type": "string"},
                        "location": {"type": "string"},
                    }
                }
            }
        ]
    }

    search_result = {
        "result": json.dumps({
            "market": "CRM",
            "location": "Brasil",
            "results": [
                {"title": "Salesforce Brasil", "url": "salesforce.com", "snippet": "CRM lider..."},
                {"title": "Pipedrive PT", "url": "pipedrive.com", "snippet": "CRM para vendas..."},
            ]
        })
    }

    with respx.mock:
        # Mock para listagem de ferramentas (GET /mcp)
        respx.get("http://localhost:8001/mcp").mock(
            return_value=httpx.Response(200, json=tools_response)
        )
        # Mock para chamada de ferramenta (POST /mcp)
        respx.post("http://localhost:8001/mcp").mock(
            return_value=httpx.Response(200, json=search_result)
        )
        yield


@pytest.mark.asyncio
async def test_researcher_returns_structured_data(mock_research_mcp):
    """Researcher deve retornar research_result estruturado."""
    state = {
        "query": "analise CRM Brasil",
        "research_result": None,
        "analysis_result": None,
        "report": None,
        "next": "",
        "messages": [],
        "completed_agents": [],
    }

    result = await researcher_node_async(state)

    # Deve retornar research_result como string nao vazia
    assert "research_result" in result
    assert isinstance(result["research_result"], str)
    assert len(result["research_result"]) > 0

    # Deve retornar messages como lista
    assert "messages" in result
    assert isinstance(result["messages"], list)
