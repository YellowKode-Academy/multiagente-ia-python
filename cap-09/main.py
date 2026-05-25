# main.py - versao cap-09
import sys
import time
from dotenv import load_dotenv
from src.orchestrator.graph import graph
from src.orchestrator.tracing import get_run_config

load_dotenv()


def main():
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else \
        "analise competitiva para um SaaS de gestao de projetos no Brasil"

    print(f"Analisando: {query}\n")
    print(f"Trace disponivel em: http://localhost:3000")

    # Configuracao de run com Langfuse
    run_config = get_run_config(query=query)

    start = time.time()
    result = graph.invoke(
        {
            "query": query,
            "research_result": None,
            "analysis_result": None,
            "report": None,
            "next": "",
            "messages": [],
            "completed_agents": [],
        },
        config=run_config,  # passa o handler Langfuse
    )
    elapsed = time.time() - start

    # Flush para garantir que os dados foram enviados ao Langfuse
    if run_config.get("callbacks"):
        run_config["callbacks"][0].flush()

    print(f"\nStatus: {result.get('next')}")
    print(f"Tempo total: {elapsed:.1f}s")
    print(f"Relatorio: relatorio.md")
    print(f"\nVeja o trace em: http://localhost:3000/traces")


if __name__ == "__main__":
    main()
