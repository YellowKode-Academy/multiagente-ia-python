# tests/integration/test_full_flow.py
import pytest
from unittest.mock import patch, MagicMock


def build_mocked_graph(mock_research, mock_analysis, mock_report):
    """Constroi grafo com nos mockados para testes de integracao."""
    with patch("src.agents.researcher.agent.researcher_node", return_value=mock_research), \
         patch("src.agents.analyzer.agent.analyzer_node", return_value=mock_analysis), \
         patch("src.agents.reporter.agent.reporter_node", return_value=mock_report):
        from src.orchestrator.graph import build_graph
        return build_graph()


MOCK_RESEARCH = {
    "research_result": '{"competitors": [{"name": "Asana", "differentiator": "timeline", "market_presence": "alta"}]}',
    "messages": [],
    "completed_agents": ["researcher"],
}

MOCK_ANALYSIS = {
    "analysis_result": '{"scored_competitors": [{"name": "Asana", "score": 82, "threat_level": "alta"}], "market_gaps": [], "recommended_positioning": "focar em PMEs", "analysis_confidence": 0.75}',
    "messages": [],
    "completed_agents": ["analyzer"],
}

MOCK_REPORT = {
    "report": "# Relatorio\n\n## Resumo Executivo\n\nMercado de CRM no Brasil apresenta crescimento de 18% ao ano. Principais players: Salesforce, Pipedrive, HubSpot. Oportunidade para solucoes voltadas a PMEs.\n\n## Recomendacao\n\nFocar em segmento de PMEs com precificacao agressiva.",
    "messages": [],
}

INITIAL_STATE = {
    "query": "analise CRM Brasil",
    "research_result": None,
    "analysis_result": None,
    "report": None,
    "next": "",
    "phase": "",
    "messages": [],
    "completed_agents": [],
}


def test_full_flow_completes():
    """Fluxo completo deve terminar com status 'finish'."""
    g = build_mocked_graph(MOCK_RESEARCH, MOCK_ANALYSIS, MOCK_REPORT)
    result = g.invoke(INITIAL_STATE)

    assert result.get("next") == "finish"
    assert result.get("research_result") is not None
    assert result.get("analysis_result") is not None
    assert result.get("report") is not None


def test_full_flow_state_fields():
    """Todos os campos de resultado devem estar preenchidos ao final."""
    g = build_mocked_graph(MOCK_RESEARCH, MOCK_ANALYSIS, MOCK_REPORT)
    result = g.invoke(INITIAL_STATE)

    assert "research_result" in result
    assert "analysis_result" in result
    assert "report" in result
    assert len(result["report"]) > 100
