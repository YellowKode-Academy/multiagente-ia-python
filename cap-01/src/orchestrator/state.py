# src/orchestrator/state.py
from typing import Annotated, Optional
from typing_extensions import TypedDict
import operator


class MarketIntelligenceState(TypedDict):
    query: str                           # pedido original do usuario
    research_result: Optional[str]       # resultado do agente pesquisa
    analysis_result: Optional[str]       # resultado do agente analise
    report: Optional[str]               # relatorio final
    next: str                           # proximo agente a chamar
    messages: Annotated[list, operator.add]  # historico de mensagens
