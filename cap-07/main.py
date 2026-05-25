# main.py - versao cap-07
import sys
import time
from dotenv import load_dotenv
from src.orchestrator.graph import graph

load_dotenv()


def main():
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else \
        "analise competitiva para um SaaS de CRM no Brasil"

    print(f"Analisando (modo paralelo): {query}\n")

    start = time.time()
    result = graph.invoke({
        "query": query,
        "research_result": None,
        "analysis_result": None,
        "report": None,
        "next": "",
        "messages": [],
        "completed_agents": [],
    })
    elapsed = time.time() - start

    print(f"Status: {result.get('next')}")
    print(f"Tempo total: {elapsed:.1f}s")
    print(f"Agentes concluidos: {result.get('completed_agents', [])}")

    if result.get("report"):
        print("\n--- Previa do Relatorio ---")
        print(result["report"][:400])


if __name__ == "__main__":
    main()
