# main.py - versao cap-03
import time
from dotenv import load_dotenv
from src.orchestrator.graph import graph

load_dotenv()


def main():
    initial_state = {
        "query": "analise competitiva para um SaaS de gestao de projetos no Brasil",
        "research_result": None,
        "analysis_result": None,
        "report": None,
        "next": "",
        "messages": [],
    }

    print("Iniciando analise...\n")

    start = time.time()
    result = graph.invoke(initial_state)
    elapsed = time.time() - start

    print("=== PESQUISA ===")
    research = result.get("research_result", "")
    print(research[:400] + "..." if len(research) > 400 else research)

    print("\n=== ANALISE ===")
    analysis = result.get("analysis_result", "")
    print(analysis[:400] + "..." if len(analysis) > 400 else analysis)

    print(f"\n=== STATUS FINAL ===")
    print(f"Proximo: {result.get('next')} (FINISH = sistema encerrou corretamente)")
    print(f"\nTempo total: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
