# tests/integration/test_full_flow.py
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from src.orchestrator.graph import graph


@pytest.fixture
def mock_all_agents():
    """Mocka todos os agentes para retornar dados fixos."""

    mock_research = {
        "research_result": '{"competitors": [{"name": "Asana", "differentiator": "timeline", "market_presence": "alta"}]}',
        "messages": [],
        "completed_agents": ["researcher"],
    }

    mock_analysis = {
        "analysis_result": '{"scored_competitors": [{"name": "Asana", "score": 82, "threat_level": "alta"}], "market_gaps": [], "recommended_positioning": "focar em PMEs", "analysis_confidence": 0.75}',
        "messages": [],
        "completed_agents": ["analyzer"],
    }

    mock_report = {
        "report": "# Relatorio\n\n## Resumo Executivo\n\nMercado analisado...",
        "messages": [],
    }

    with patch("src.agents.researcher.agent.researcher_node", return_value=mock_research), \
         patch("src.agents.analyzer.agent.analyzer_node", return_value=mock_analysis), \
         patch("src.agents.reporter.agent.reporter_node", return_value=mock_report):
        yield


def test_full_flow_completes(mock_all_agents):
    """Fluxo completo deve terminar com status 'finish'."""
    initial_state = {
        "query": "analise CRM Brasil",
        "research_result": None,
        "analysis_result": None,
        "report": None,
        "next": "",
        "messages": [],
        "completed_agents": [],
    }

    result = graph.invoke(initial_state)

    assert result.get("next") == "finish"
    assert result.get("research_result") is not None
    assert result.get("analysis_result") is not None
    assert result.get("report") is not None


def test_full_flow_state_fields(mock_all_agents):
    """Todos os campos de resultado devem estar preenchidos ao final."""
    initial_state = {
        "query": "analise CRM Brasil",
        "research_result": None,
        "analysis_result": None,
        "report": None,
        "next": "",
        "messages": [],
        "completed_agents": [],
    }

    result = graph.invoke(initial_state)

    # Verificar campos
    assert "research_result" in result
    assert "analysis_result" in result
    assert "report" in result
    assert len(result["report"]) > 100  # relatorio nao vazio
