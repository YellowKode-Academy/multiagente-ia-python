# src/orchestrator/supervisor.py - versao cap-07
from langgraph.types import Send
from .state import MarketIntelligenceState


def supervisor_node(state: MarketIntelligenceState) -> dict | list:
    """
    No supervisor: roteia para agentes em paralelo ou sequencialmente.

    Retorna dict (roteamento sequencial via conditional_edges)
    ou lista de Send() (roteamento paralelo via fan-out).
    """
    research_done = bool(state.get("research_result"))
    analysis_done = bool(state.get("analysis_result"))
    report_done = bool(state.get("report"))

    # Estado inicial: nada foi feito - fan-out paralelo
    if not research_done and not analysis_done:
        return [
            Send("researcher", {"query": state["query"]}),
            Send("analyzer", {"query": state["query"]}),
        ]

    # Pesquisa e analise prontas - chamar o reporter
    if research_done and analysis_done and not report_done:
        return {"next": "reporter"}

    # Tudo pronto - encerrar
    if report_done:
        return {"next": "finish"}

    # Estado intermediario: nao deve acontecer com fan-out correto
    return {"next": "finish"}
