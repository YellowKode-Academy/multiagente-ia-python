# main.py - versao cap-04
# Requer: python -m src.agents.researcher.mcp_server.server (Terminal 1)
from dotenv import load_dotenv
from src.orchestrator.graph import graph

load_dotenv()


def main():
    result = graph.invoke({
        "query": "analise competitiva para um SaaS de gestao de projetos no Brasil",
        "research_result": None,
        "analysis_result": None,
        "report": None,
        "next": "",
        "messages": [],
    })

    print("=== RESULTADO DA PESQUISA (via MCP) ===")
    if result.get("research_result"):
        print(result["research_result"][:500] + "...")

    print(f"\nProximo passo: {result.get('next', 'END')}")


if __name__ == "__main__":
    main()
