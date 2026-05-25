# main.py
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

    print(f"Supervisor decidiu: {result['next']}")
    print(f"Estado final: {result}")

    # Visualizar o grafo (opcional)
    # print(graph.get_graph().draw_ascii())


if __name__ == "__main__":
    main()
