# src/orchestrator/graph.py - versao cap-08
from langgraph.graph import StateGraph, END
from langgraph.types import Send
from .state import MarketIntelligenceState
from .supervisor import supervisor_node_fanout
from .aggregator import aggregator_node
from src.agents.researcher.agent import researcher_node
from src.agents.analyzer.agent import analyzer_node
from src.agents.reporter.agent import reporter_node


def route_aggregator(state: MarketIntelligenceState) -> str:
    """Roteamento do aggregator: reporter se pronto, waiting se nao."""
    return state.get("next", "reporter")


def build_graph() -> StateGraph:
    workflow = StateGraph(MarketIntelligenceState)

    # Nos
    workflow.add_node("supervisor", supervisor_node_fanout)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("analyzer", analyzer_node)
    workflow.add_node("aggregator", aggregator_node)   # cap-08
    workflow.add_node("reporter", reporter_node)

    workflow.set_entry_point("supervisor")

    # Supervisor faz o fan-out
    # route_after_supervisor le state["next"] apos o no executar - nao re-executa o supervisor
    def route_after_supervisor(state: MarketIntelligenceState):
        return state.get("next", "finish")

    workflow.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {
            "reporter": "reporter",  # apos aggregator sinalizar
            "finish": END,
        }
    )

    # Apos researcher e analyzer, vao para o aggregator (nao o supervisor)
    workflow.add_edge("researcher", "aggregator")  # cap-08
    workflow.add_edge("analyzer", "aggregator")    # cap-08

    # O aggregator roteia para reporter ou aguarda
    workflow.add_conditional_edges(
        "aggregator",
        route_aggregator,
        {
            "reporter": "reporter",
            "waiting": "aggregator",  # loop de espera (nao deve acontecer em pratica)
        }
    )

    # Reporter vai para supervisor (para o supervisor verificar "finish")
    workflow.add_edge("reporter", "supervisor")

    return workflow.compile()


graph = build_graph()
