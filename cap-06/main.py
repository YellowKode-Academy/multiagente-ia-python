# main.py - versao cap-06
# Requer tres terminais com MCP servers:
# Terminal 1: python -m src.agents.researcher.mcp_server.server  (porta 8001)
# Terminal 2: python -m src.agents.analyzer.mcp_server.server    (porta 8002)
# Terminal 3: python -m src.agents.reporter.mcp_server.server    (porta 8003)
import sys
import time
from dotenv import load_dotenv
from src.orchestrator.graph import graph

load_dotenv()


def main():
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else \
        "analise competitiva para um SaaS de gestao de projetos no Brasil"

    print(f"Analisando: {query}\n")

    start = time.time()
    result = graph.invoke({
        "query": query,
        "research_result": None,
        "analysis_result": None,
        "report": None,
        "next": "",
        "messages": [],
    })
    elapsed = time.time() - start

    print(f"Status: {result.get('next')}")
    print(f"Tempo total: {elapsed:.1f}s")
    print(f"\nRelatorio salvo em: relatorio.md")

    # Mostrar primeiras linhas do relatorio
    if result.get("report"):
        print("\n--- Previa do Relatorio ---")
        print(result["report"][:600])


if __name__ == "__main__":
    main()
