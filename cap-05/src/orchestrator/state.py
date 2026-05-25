# src/orchestrator/state.py
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
