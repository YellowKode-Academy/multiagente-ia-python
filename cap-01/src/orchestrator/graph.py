# src/orchestrator/graph.py
from langgraph.graph import StateGraph, END
from .state import MarketIntelligenceState
from .supervisor import supervisor_node


def route_next(state: MarketIntelligenceState) -> str:
    """Funcao de roteamento: le state['next'] e retorna o nome do proximo no."""
    return state.get("next", "researcher")


def build_graph() -> StateGraph:
    workflow = StateGraph(MarketIntelligenceState)

    # No supervisor - o unico no por enquanto
    workflow.add_node("supervisor", supervisor_node)

    # Ponto de entrada
    workflow.set_entry_point("supervisor")

    # Roteamento condicional - por enquanto so conhece "finish"
    # Os agentes serao adicionados nos proximos capitulos
    workflow.add_conditional_edges(
        "supervisor",
        route_next,
        {
            "researcher": END,  # cap-02 vai substituir END por no real
            "analyzer": END,    # cap-03 vai substituir END por no real
            "reporter": END,    # cap-06 vai substituir END por no real
            "finish": END,
        }
    )

    return workflow.compile()


graph = build_graph()
