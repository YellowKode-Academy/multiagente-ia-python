# main.py - versao cap-05
# Requer dois terminais com MCP servers:
# Terminal 1: python -m src.agents.researcher.mcp_server.server  (porta 8001)
# Terminal 2: python -m src.agents.analyzer.mcp_server.server    (porta 8002)
import sys
import time
from dotenv import load_dotenv
from src.orchestrator.graph import graph

load_dotenv()


def main():
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else \
        "analise competitiva para um SaaS de gestao de projetos no Brasil"

    print(f"Analisando: {query}\n")
    print("Aguardando MCP servers em localhost:8001 (researcher) e localhost:8002 (analyzer)...\n")

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

    if result.get("analysis_result"):
        print("\n--- Resultado da Analise ---")
        print(str(result["analysis_result"])[:600])


if __name__ == "__main__":
    main()
