# src/orchestrator/graph.py - versao cap-07
from langgraph.graph import StateGraph, END
from langgraph.types import Send
from .state import MarketIntelligenceState
from .supervisor import supervisor_node
from src.agents.researcher.agent import researcher_node
from src.agents.analyzer.agent import analyzer_node
from src.agents.reporter.agent import reporter_node


def route_after_supervisor(state: MarketIntelligenceState):
    """
    Funcao de roteamento - le o estado APOS o supervisor ter executado.

    O supervisor ja escreveu state["next"] ou retornou Send() via lista.
    Esta funcao so le o resultado - NAO re-executa o supervisor.
    """
    next_val = state.get("next", "finish")
    return next_val


def build_graph() -> StateGraph:
    workflow = StateGraph(MarketIntelligenceState)

    # Nos
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("analyzer", analyzer_node)
    workflow.add_node("reporter", reporter_node)

    workflow.set_entry_point("supervisor")

    # Roteamento do supervisor - le state["next"] apos o no executar
    workflow.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {
            "researcher": "researcher",
            "analyzer": "analyzer",
            "reporter": "reporter",
            "finish": END,
        }
    )

    # Apos cada agente, volta ao supervisor
    # (ou para o aggregator no cap-08)
    workflow.add_edge("researcher", "supervisor")
    workflow.add_edge("analyzer", "supervisor")
    workflow.add_edge("reporter", "supervisor")

    return workflow.compile()


graph = build_graph()
