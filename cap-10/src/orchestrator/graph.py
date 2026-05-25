# src/orchestrator/graph.py - versao cap-08/10
from langgraph.graph import StateGraph, END
from .state import MarketIntelligenceState
from .supervisor import supervisor_node_fanout
from .aggregator import aggregator_node
from src.agents.researcher.agent import researcher_node
from src.agents.analyzer.agent import analyzer_node
from src.agents.reporter.agent import reporter_node


def route_aggregator(state: MarketIntelligenceState) -> str:
    return state.get("next", "reporter")


def build_graph() -> StateGraph:
    workflow = StateGraph(MarketIntelligenceState)

    workflow.add_node("supervisor", supervisor_node_fanout)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("analyzer", analyzer_node)
    workflow.add_node("aggregator", aggregator_node)
    workflow.add_node("reporter", reporter_node)

    workflow.set_entry_point("supervisor")

    def route_after_supervisor(state: MarketIntelligenceState):
        return state.get("next", "finish")

    workflow.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {"reporter": "reporter", "finish": END}
    )

    workflow.add_edge("researcher", "aggregator")
    workflow.add_edge("analyzer", "aggregator")

    workflow.add_conditional_edges(
        "aggregator",
        route_aggregator,
        {"reporter": "reporter", "waiting": "aggregator"}
    )

    workflow.add_edge("reporter", "supervisor")

    return workflow.compile()


graph = build_graph()
