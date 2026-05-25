# src/orchestrator/supervisor.py - versao cap-08
from langgraph.types import Send
from .state import MarketIntelligenceState


def supervisor_node_fanout(state: MarketIntelligenceState):
    """
    Supervisor simplificado para o padrao fan-out/fan-in.

    - Estado inicial: fan-out paralelo para researcher e analyzer
    - Apos reporter: verificar FINISH
    """
    research_done = bool(state.get("research_result"))
    analysis_done = bool(state.get("analysis_result"))
    report_done = bool(state.get("report"))

    # Estado inicial: fan-out paralelo
    if not research_done and not analysis_done:
        return [
            Send("researcher", {"query": state["query"]}),
            Send("analyzer", {"query": state["query"]}),
        ]

    # Reporter terminou: encerrar
    if report_done:
        return {"next": "finish"}

    # Estado intermediario (nao esperado no fluxo normal)
    return {"next": "finish"}
