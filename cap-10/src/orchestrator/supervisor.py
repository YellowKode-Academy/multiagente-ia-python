# src/orchestrator/supervisor.py
from langgraph.types import Send
from .state import MarketIntelligenceState


def supervisor_node(state: MarketIntelligenceState) -> dict:
    """Supervisor determina a fase de execucao."""
    research_done = bool(state.get("research_result"))
    analysis_done = bool(state.get("analysis_result"))
    report_done = bool(state.get("report"))

    if not research_done and not analysis_done:
        return {"phase": "fanout"}

    if report_done:
        return {"next": "finish", "phase": "done"}

    if research_done and analysis_done:
        return {"next": "reporter", "phase": "report"}

    return {"next": "finish", "phase": "done"}


def route_after_supervisor(state: MarketIntelligenceState):
    """Roteia apos supervisor: fan-out com Send ou string para aresta nomeada."""
    if state.get("phase") == "fanout":
        return [
            Send("researcher", {"query": state["query"]}),
            Send("analyzer", {"query": state["query"]}),
        ]
    return state.get("next", "finish")


# Keep old name as alias for backward compatibility
supervisor_node_fanout = supervisor_node
