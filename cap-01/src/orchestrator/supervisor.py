# src/orchestrator/supervisor.py
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from .state import MarketIntelligenceState

llm = ChatAnthropic(model="claude-sonnet-4-6")

SUPERVISOR_SYSTEM_PROMPT = """Voce e o supervisor de um sistema de inteligencia competitiva.
Seu trabalho e decidir qual especialista deve trabalhar a seguir.

Especialistas disponiveis:
- researcher: busca dados sobre mercado, concorrentes e tendencias
- analyzer: analisa os dados coletados e calcula scores competitivos
- reporter: gera o relatorio final com base na analise

Regras de roteamento:
1. Se research_result estiver vazio: chame researcher
2. Se research_result estiver preenchido e analysis_result estiver vazio: chame analyzer
3. Se research_result E analysis_result estiverem preenchidos e report estiver vazio: chame reporter
4. Se research_result, analysis_result E report estiverem preenchidos: retorne FINISH

Responda APENAS com o nome do proximo especialista ou FINISH.
Nao explique o motivo. Nao adicione texto extra."""


def supervisor_node(state: MarketIntelligenceState) -> dict:
    """No supervisor: decide o proximo agente baseado no estado atual."""

    context = f"""Estado atual:
- query: {state.get('query', '')}
- research_result: {'[preenchido]' if state.get('research_result') else '[vazio]'}
- analysis_result: {'[preenchido]' if state.get('analysis_result') else '[vazio]'}
- report: {'[preenchido]' if state.get('report') else '[vazio]'}

Qual especialista deve trabalhar a seguir?"""

    response = llm.invoke([
        SystemMessage(content=SUPERVISOR_SYSTEM_PROMPT),
        HumanMessage(content=context),
    ])

    next_agent = response.content.strip().lower()

    # validacao defensiva
    valid_agents = {"researcher", "analyzer", "reporter", "finish"}
    if next_agent not in valid_agents:
        next_agent = "researcher"  # fallback seguro

    return {"next": next_agent}
