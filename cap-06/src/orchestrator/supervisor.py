# src/orchestrator/supervisor.py - versao cap-03 (sem alteracoes caps 04-06)
from .state import MarketIntelligenceState


def supervisor_node(state: MarketIntelligenceState) -> dict:
    """No supervisor: decide o proximo agente com base no estado atual."""

    if not state.get("research_result"):
        return {"next": "researcher"}

    if not state.get("analysis_result"):
        return {"next": "analyzer"}

    if not state.get("report"):
        return {"next": "reporter"}

    return {"next": "finish"}
