# src/orchestrator/aggregator.py
from .state import MarketIntelligenceState


def aggregator_node(state: MarketIntelligenceState) -> dict:
    """
    No de sincronizacao fan-in.

    Aguarda que researcher E analyzer terminem antes de prosseguir ao reporter.
    Combina os resultados em um campo unificado para facilitar o reporter.
    """
    research_result = state.get("research_result")
    analysis_result = state.get("analysis_result")

    # Verificacao de completude
    research_done = bool(research_result)
    analysis_done = bool(analysis_result)

    if not research_done or not analysis_done:
        # Estado incompleto - nao deve acontecer em operacao normal
        # mas e um safeguard contra race conditions
        return {
            "next": "waiting",  # sinal para o grafo aguardar
        }

    # Ambos os agentes terminaram - preparar dados para o reporter
    combined_data = {
        "research_summary": research_result[:200] if len(research_result) > 200 else research_result,
        "analysis_summary": analysis_result[:200] if len(analysis_result) > 200 else analysis_result,
        "status": "ready",
    }

    return {
        "next": "reporter",
        # combined_data disponivel para debug; reporter usa research_result e analysis_result diretamente
    }
