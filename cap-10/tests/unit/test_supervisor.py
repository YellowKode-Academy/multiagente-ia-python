# tests/unit/test_supervisor.py
import pytest
from langgraph.types import Send
from src.orchestrator.supervisor import supervisor_node, route_after_supervisor

# backward-compat alias used in some tests
supervisor_node_fanout = supervisor_node


class TestSupervisorRouting:
    """Testa o roteamento do supervisor baseado no estado."""

    def test_initial_state_returns_fanout(self):
        """Estado vazio: supervisor_node define phase=fanout, route retorna Send list."""
        state = {
            "query": "analise SaaS CRM Brasil",
            "research_result": None,
            "analysis_result": None,
            "report": None,
            "next": "",
            "phase": "",
            "messages": [],
            "completed_agents": [],
        }

        # Node sets phase
        node_result = supervisor_node(state)
        assert node_result.get("phase") == "fanout"

        # Routing function returns Send list
        updated_state = {**state, **node_result}
        result = route_after_supervisor(updated_state)

        assert isinstance(result, list)
        assert len(result) == 2
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
            "phase": "",
            "messages": [],
            "completed_agents": [],
        }

        result = supervisor_node_fanout(state)

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
            "phase": "",
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
            "phase": "",
            "messages": [],
            "completed_agents": [],
        }

        result = supervisor_node_fanout(state)

        if isinstance(result, dict):
            assert result.get("next") != "reporter"
