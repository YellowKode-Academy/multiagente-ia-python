# tests/unit/test_aggregator.py
import pytest
from src.orchestrator.aggregator import aggregator_node


class TestAggregator:
    """Testa o no aggregator (ponto de sincronizacao fan-in)."""

    def test_both_results_ready_returns_reporter(self):
        """Com pesquisa e analise prontas, aggregator avanca para reporter."""
        state = {
            "query": "teste",
            "research_result": '{"competitors": [{"name": "Asana"}]}',
            "analysis_result": '{"scored_competitors": [{"name": "Asana", "score": 80}]}',
            "report": None,
            "next": "",
            "messages": [],
            "completed_agents": ["researcher", "analyzer"],
        }

        result = aggregator_node(state)

        assert result.get("next") == "reporter"

    def test_only_research_not_ready(self):
        """Com apenas research_result, aggregator nao avanca."""
        state = {
            "query": "teste",
            "research_result": '{"competitors": [...]}',
            "analysis_result": None,  # vazio
            "report": None,
            "next": "",
            "messages": [],
            "completed_agents": ["researcher"],
        }

        result = aggregator_node(state)

        assert result.get("next") != "reporter"

    def test_empty_state_not_ready(self):
        """Estado completamente vazio - nao avanca."""
        state = {
            "query": "teste",
            "research_result": None,
            "analysis_result": None,
            "report": None,
            "next": "",
            "messages": [],
            "completed_agents": [],
        }

        result = aggregator_node(state)

        assert result.get("next") != "reporter"
