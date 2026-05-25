# tests/unit/test_supervisor.py
import pytest
from langgraph.types import Send
from src.orchestrator.supervisor import supervisor_node_fanout


class TestSupervisorRouting:
    """Testa o roteamento do supervisor baseado no estado."""

    def test_initial_state_returns_fanout(self):
        """Estado vazio deve retornar fan-out paralelo."""
        state = {
            "query": "analise SaaS CRM Brasil",
            "research_result": None,
            "analysis_result": None,
            "report": None,
            "next": "",
            "messages": [],
            "completed_agents": [],
        }

        result = supervisor_node_fanout(state)

        # Deve retornar lista de Send()
        assert isinstance(result, list)
        assert len(result) == 2

        # Verificar os alvos do Send()
        targets = [send.node for send in result]
        assert "researcher" in targets
        assert "analyzer" in targets

    def test_both_done_returns_reporter(self):
        """research_result + analysis_result preenchidos -> reporter."""
        state = {
            "query": "analise SaaS CRM Brasil",
            "research_result": '{"competitors": [...]}',
            "analysis_result": '{"scored_competitors": [...]}',
            "report": None,
            "next": "",
            "messages": [],
            "completed_agents": [],
        }

        result = supervisor_node_fanout(state)

        # Deve retornar dict com next="reporter"
        assert isinstance(result, dict)
        assert result.get("next") == "reporter"

    def test_all_done_returns_finish(self):
        """Todos os campos preenchidos -> FINISH."""
        state = {
            "query": "analise SaaS CRM Brasil",
            "research_result": '{"competitors": [...]}',
            "analysis_result": '{"scored_competitors": [...]}',
            "report": "# Relatorio...",
            "next": "",
            "messages": [],
            "completed_agents": [],
        }

        result = supervisor_node_fanout(state)

        assert isinstance(result, dict)
        assert result.get("next") == "finish"

    def test_only_research_done_does_not_advance(self):
        """research_result preenchido mas analysis_result vazio -> nao avanca."""
        state = {
            "query": "analise SaaS CRM Brasil",
            "research_result": '{"competitors": [...]}',
            "analysis_result": None,
            "report": None,
            "next": "",
            "messages": [],
            "completed_agents": [],
        }

        result = supervisor_node_fanout(state)

        # Com apenas research_result, supervisor nao deve avancar para reporter
        # Deve aguardar analysis_result
        if isinstance(result, dict):
            assert result.get("next") != "reporter"
