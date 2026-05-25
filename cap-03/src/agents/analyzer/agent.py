# src/agents/analyzer/agent.py
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from src.orchestrator.state import MarketIntelligenceState
import json

llm = ChatAnthropic(model="claude-sonnet-4-6")

ANALYZER_SYSTEM_PROMPT = """Voce e um analista de inteligencia competitiva.
Voce recebe dados de pesquisa de mercado e produz analise estruturada.

Para cada analise:
1. Score cada concorrente de 0-100 baseado em: presenca de mercado, diferenciacao, momentum
2. Identifique os 3 principais gaps de mercado que a analise revela
3. Classifique os concorrentes por ameaca (alta/media/baixa)
4. Identifique o posicionamento ideal para uma nova entrada no mercado

Retorne em JSON com os campos:
- scored_competitors: lista com name, score, threat_level
- market_gaps: lista de 3 gaps identificados
- recommended_positioning: string com o posicionamento recomendado
- analysis_confidence: numero 0-1 indicando confianca nos dados

Baseie-se APENAS nos dados fornecidos. Nao invente dados que nao estao na pesquisa."""


@tool
def score_competitor(name: str, differentiator: str, market_presence: str) -> str:
    """Calcula score de ameaca competitiva baseado em criterios objetivos."""
    # Logica de scoring simplificada para o cap-03
    # No cap-05, isso vai para o MCP Server de analise
    score_map = {
        "alta": 80,
        "media": 55,
        "baixa": 30,
    }
    base_score = score_map.get(market_presence.lower(), 50)
    # Ajuste por comprimento do diferenciador (proxy para especificidade)
    adjustment = min(20, len(differentiator) // 10)
    return json.dumps({"name": name, "score": min(100, base_score + adjustment)})


@tool
def identify_market_gaps(competitors_json: str) -> str:
    """Identifica gaps de mercado baseado na lista de concorrentes."""
    # Placeholder - no cap-05, ferramenta real no MCP Server
    competitors = json.loads(competitors_json)
    gaps = [
        "Ausencia de solucao focada em PMEs com menos de 10 funcionarios",
        "Nenhum player com interface em portugues e suporte local",
        "Integracao com ferramentas fiscais brasileiras nao coberta",
    ]
    return json.dumps({"gaps": gaps[:3]})


tools = [score_competitor, identify_market_gaps]

analyzer_agent = create_react_agent(
    model=llm,
    tools=tools,
    state_modifier=ANALYZER_SYSTEM_PROMPT,
)


def analyzer_node(state: MarketIntelligenceState) -> dict:
    """No analisador: processa research_result e atualiza analysis_result."""

    research_data = state.get("research_result", "")

    result = analyzer_agent.invoke({
        "messages": [HumanMessage(
            content=f"Analise estes dados de pesquisa:\n\n{research_data}"
        )]
    })

    analysis_result = result["messages"][-1].content

    return {
        "analysis_result": analysis_result,
        "messages": result["messages"],
    }
