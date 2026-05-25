# tests/unit/test_analysis_tools.py
import pytest
import json
from src.agents.analyzer.mcp_server.tools.scorer import score_competitor, score_competitors_batch
from src.agents.analyzer.mcp_server.tools.gap_finder import identify_market_gaps


class TestScorer:
    """Testa as ferramentas de scoring do analysis-mcp-server."""

    def test_alta_presence_scores_high(self):
        """Concorrente com presenca alta deve ter score >= 60."""
        result_str = score_competitor(
            name="Salesforce",
            differentiator="CRM enterprise com 200+ integracoes e AI nativa",
            market_presence="alta",
        )
        result = json.loads(result_str)
        assert result["score"] >= 60
        assert result["threat_level"] == "alta"

    def test_baixa_presence_scores_low(self):
        """Concorrente com presenca baixa deve ter score < 50."""
        result_str = score_competitor(
            name="Startup Desconhecida",
            differentiator="CRM simples",
            market_presence="baixa",
        )
        result = json.loads(result_str)
        assert result["score"] < 50

    def test_batch_sorted_by_score(self):
        """Batch deve retornar concorrentes ordenados por score decrescente."""
        competitors = [
            {"name": "A", "differentiator": "simples", "market_presence": "baixa"},
            {"name": "B", "differentiator": "avancado com muitas features enterprise", "market_presence": "alta"},
        ]

        result_str = score_competitors_batch(json.dumps(competitors))
        result = json.loads(result_str)

        scored = result["scored_competitors"]
        assert len(scored) == 2
        assert scored[0]["score"] >= scored[1]["score"]  # ordenado por score desc

    def test_invalid_presence_fallback(self):
        """market_presence invalido deve usar fallback sem lancar excecao."""
        result_str = score_competitor(
            name="Test",
            differentiator="test",
            market_presence="invalido",  # valor invalido
        )
        result = json.loads(result_str)
        assert "score" in result  # nao deve lancar excecao


class TestGapFinder:
    """Testa a identificacao de gaps de mercado."""

    def test_identifies_portuguese_gap(self):
        """Quando nenhum concorrente tem portugues, deve identificar o gap."""
        competitors = [
            {"name": "Asana", "differentiator": "visual timeline interface"},
            {"name": "Monday.com", "differentiator": "no-code automations"},
        ]

        result_str = identify_market_gaps(json.dumps(competitors), "gestao de projetos")
        result = json.loads(result_str)

        gaps = result.get("gaps_identified", [])
        gap_texts = [g["gap"].lower() for g in gaps]

        # Pelo menos um gap deve mencionar portugues ou Brasil
        has_lang_gap = any("portugu" in g or "brasil" in g for g in gap_texts)
        assert has_lang_gap
