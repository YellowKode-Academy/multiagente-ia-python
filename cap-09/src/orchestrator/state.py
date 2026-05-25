# src/orchestrator/state.py - versao cap-07/08/09
from typing import Annotated, Optional
from typing_extensions import TypedDict
import operator


class MarketIntelligenceState(TypedDict):
    query: str
    research_result: Optional[str]
    analysis_result: Optional[str]
    report: Optional[str]
    next: str
    messages: Annotated[list, operator.add]
    completed_agents: Annotated[list, operator.add]
