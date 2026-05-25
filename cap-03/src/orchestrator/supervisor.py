# src/orchestrator/supervisor.py - versao cap-03
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from .state import MarketIntelligenceState

llm = ChatAnthropic(model="claude-sonnet-4-6")

SUPERVISOR_SYSTEM_PROMPT = """Voce e o supervisor de um sistema de inteligencia competitiva.
Seu unico trabalho e decidir quem trabalha a seguir.

Especialistas:
- researcher: coleta dados de mercado e concorrentes
- analyzer: analisa os dados coletados e gera scores competitivos
- reporter: gera o relatorio final (cap-06)

Regras (aplique NA ORDEM):
1. research_result vazio -> retorne: researcher
2. analysis_result vazio -> retorne: analyzer
3. Todos os campos preenchidos -> retorne: FINISH

IMPORTANTE: Retorne APENAS uma palavra: researcher, analyzer, reporter, ou FINISH.
Sem explicacao, sem pontuacao extra, sem aspas."""


def supervisor_node(state: MarketIntelligenceState) -> dict:
    """No supervisor: decide o proximo agente com base no estado atual."""

    # Checagem antecipada antes de chamar o LLM
    # Isso evita chamadas desnecessarias a API quando a decisao e obvia
    if not state.get("research_result"):
        return {"next": "researcher"}

    if not state.get("analysis_result"):
        return {"next": "analyzer"}

    if not state.get("report"):
        return {"next": "reporter"}

    # Todos os campos preenchidos - encerrar
    return {"next": "finish"}
