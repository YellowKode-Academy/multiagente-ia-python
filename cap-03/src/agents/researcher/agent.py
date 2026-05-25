# src/agents/researcher/agent.py
from langchain_anthropic import ChatAnthropic
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from src.orchestrator.state import MarketIntelligenceState

llm = ChatAnthropic(model="claude-sonnet-4-6")

RESEARCHER_SYSTEM_PROMPT = """Voce e um especialista em pesquisa de mercado competitivo.
Sua tarefa: coletar dados sobre concorrentes, tendencias e posicionamento de mercado.

Para cada pesquisa:
1. Busque os principais players do mercado
2. Identifique diferenciais de cada player
3. Busque dados de crescimento ou adocao quando disponiveis
4. Identifique tendencias recentes (ultimos 6 meses)

Retorne os resultados em formato estruturado JSON com os campos:
- competitors: lista de concorrentes com nome e diferencial principal
- market_trends: tendencias identificadas
- data_sources: URLs das fontes consultadas

Seja objetivo. Nao analise - apenas colete e organize."""

# Ferramentas de busca - serao substituidas por MCP no cap-04
search_tool = TavilySearch(max_results=5)
tools = [search_tool]

researcher_agent = create_react_agent(
    model=llm,
    tools=tools,
    state_modifier=RESEARCHER_SYSTEM_PROMPT,
)


def researcher_node(state: MarketIntelligenceState) -> dict:
    """No pesquisador: executa busca e atualiza research_result no estado."""

    query = state["query"]

    result = researcher_agent.invoke({
        "messages": [HumanMessage(content=f"Pesquise: {query}")]
    })

    research_result = result["messages"][-1].content

    return {
        "research_result": research_result,
        "messages": result["messages"],
    }
