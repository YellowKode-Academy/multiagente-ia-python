# src/orchestrator/aggregator.py
from .state import MarketIntelligenceState


def aggregator_node(state: MarketIntelligenceState) -> dict:
    """No de sincronizacao fan-in."""
    research_done = bool(state.get("research_result"))
    analysis_done = bool(state.get("analysis_result"))

    if not research_done or not analysis_done:
        return {"next": "waiting"}

    return {"next": "reporter"}
