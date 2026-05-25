# src/orchestrator/graph.py - versao cap-03
from langgraph.graph import StateGraph, END
from .state import MarketIntelligenceState
from .supervisor import supervisor_node
from src.agents.researcher.agent import researcher_node
from src.agents.analyzer.agent import analyzer_node  # cap-03


def route_next(state: MarketIntelligenceState) -> str:
    next_agent = state.get("next", "researcher")
    return next_agent


def build_graph() -> StateGraph:
    workflow = StateGraph(MarketIntelligenceState)

    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("analyzer", analyzer_node)  # cap-03

    workflow.set_entry_point("supervisor")

    workflow.add_conditional_edges(
        "supervisor",
        route_next,
        {
            "researcher": "researcher",
            "analyzer": "analyzer",     # no real
            "reporter": END,            # cap-06 vai substituir
            "finish": END,
        }
    )

    # Apos cada especialista, volta ao supervisor
    workflow.add_edge("researcher", "supervisor")
    workflow.add_edge("analyzer", "supervisor")  # cap-03

    return workflow.compile()


graph = build_graph()
