# src/orchestrator/supervisor.py - versao cap-08 (sem alteracoes no cap-09)
from langgraph.types import Send
from .state import MarketIntelligenceState


def supervisor_node_fanout(state: MarketIntelligenceState):
    """Supervisor com fan-out/fan-in."""
    research_done = bool(state.get("research_result"))
    analysis_done = bool(state.get("analysis_result"))
    report_done = bool(state.get("report"))

    if not research_done and not analysis_done:
        return [
            Send("researcher", {"query": state["query"]}),
            Send("analyzer", {"query": state["query"]}),
        ]

    if report_done:
        return {"next": "finish"}

    return {"next": "finish"}
