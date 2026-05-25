# src/orchestrator/graph.py - versao cap-04
# Researcher agora usa MCP; graph permanece identico ao cap-03
from langgraph.graph import StateGraph, END
from .state import MarketIntelligenceState
from .supervisor import supervisor_node
from src.agents.researcher.agent import researcher_node


def route_next(state: MarketIntelligenceState) -> str:
    return state.get("next", "researcher")


def build_graph() -> StateGraph:
    workflow = StateGraph(MarketIntelligenceState)

    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("researcher", researcher_node)

    workflow.set_entry_point("supervisor")

    workflow.add_conditional_edges(
        "supervisor",
        route_next,
        {
            "researcher": "researcher",
            "analyzer": END,
            "reporter": END,
            "finish": END,
        }
    )

    workflow.add_edge("researcher", "supervisor")

    return workflow.compile()


graph = build_graph()
