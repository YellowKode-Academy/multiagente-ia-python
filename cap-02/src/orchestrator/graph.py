# src/orchestrator/graph.py - versao cap-02
from langgraph.graph import StateGraph, END
from .state import MarketIntelligenceState
from .supervisor import supervisor_node
from src.agents.researcher.agent import researcher_node  # cap-02


def route_next(state: MarketIntelligenceState) -> str:
    return state.get("next", "researcher")


def build_graph() -> StateGraph:
    workflow = StateGraph(MarketIntelligenceState)

    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("researcher", researcher_node)  # cap-02

    workflow.set_entry_point("supervisor")

    workflow.add_conditional_edges(
        "supervisor",
        route_next,
        {
            "researcher": "researcher",   # aponta para no real
            "analyzer": END,              # cap-03 vai substituir
            "reporter": END,              # cap-06 vai substituir
            "finish": END,
        }
    )

    # Apos o pesquisador, sempre volta para o supervisor
    workflow.add_edge("researcher", "supervisor")  # cap-02

    return workflow.compile()


graph = build_graph()
