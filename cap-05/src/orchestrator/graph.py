# src/orchestrator/graph.py - versao cap-05
# Dois MCP servers: research (8001) e analysis (8002)
from langgraph.graph import StateGraph, END
from .state import MarketIntelligenceState
from .supervisor import supervisor_node
from src.agents.researcher.agent import researcher_node
from src.agents.analyzer.agent import analyzer_node


def route_next(state: MarketIntelligenceState) -> str:
    return state.get("next", "researcher")


def build_graph() -> StateGraph:
    workflow = StateGraph(MarketIntelligenceState)

    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("analyzer", analyzer_node)

    workflow.set_entry_point("supervisor")

    workflow.add_conditional_edges(
        "supervisor",
        route_next,
        {
            "researcher": "researcher",
            "analyzer": "analyzer",
            "reporter": END,
            "finish": END,
        }
    )

    workflow.add_edge("researcher", "supervisor")
    workflow.add_edge("analyzer", "supervisor")

    return workflow.compile()


graph = build_graph()
