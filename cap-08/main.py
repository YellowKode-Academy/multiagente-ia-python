# main.py - versao cap-08
import sys
import time
from dotenv import load_dotenv
from src.orchestrator.graph import graph

load_dotenv()


def main():
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else \
        "analise competitiva SaaS de CRM Brasil"

    print(f"Analisando (fan-out/fan-in): {query}\n")

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

    # Visualizar o grafo
    # print(graph.get_graph().draw_ascii())


if __name__ == "__main__":
    main()
