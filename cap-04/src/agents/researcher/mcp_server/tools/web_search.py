# src/agents/researcher/mcp_server/tools/web_search.py
import os
import json
import httpx

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
TAVILY_BASE_URL = "https://api.tavily.com"


async def search_web(query: str, max_results: int = 5) -> str:
    """
    Busca informacoes na web sobre um topico especifico.
    Retorna JSON com titulo, URL, conteudo e score de relevancia.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{TAVILY_BASE_URL}/search",
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "max_results": max_results,
                "search_depth": "advanced",
            },
            timeout=30.0,
        )
        response.raise_for_status()
        data = response.json()

    results = [
        {
            "title": r["title"],
            "url": r["url"],
            "content": r["content"][:500],  # limite para nao estourar contexto
            "score": r.get("score", 0),
        }
        for r in data.get("results", [])
    ]

    return json.dumps({"query": query, "results": results}, ensure_ascii=False)


async def search_competitors(market: str, location: str = "Brasil") -> str:
    """
    Busca especificamente concorrentes em um mercado/nicho.
    Combina multiplas queries para cobrir diferentes angulos.
    """
    queries = [
        f"principais players {market} {location} 2026",
        f"melhores ferramentas {market} {location}",
        f"alternativas {market} software {location}",
    ]

    all_results = []
    async with httpx.AsyncClient() as client:
        for query in queries:
            response = await client.post(
                f"{TAVILY_BASE_URL}/search",
                json={
                    "api_key": TAVILY_API_KEY,
                    "query": query,
                    "max_results": 3,
                },
                timeout=30.0,
            )
            if response.status_code == 200:
                data = response.json()
                all_results.extend(data.get("results", [])[:3])

    # Deduplicar por URL
    seen_urls = set()
    unique_results = []
    for r in all_results:
        if r["url"] not in seen_urls:
            seen_urls.add(r["url"])
            unique_results.append({
                "title": r["title"],
                "url": r["url"],
                "snippet": r["content"][:300],
            })

    return json.dumps({
        "market": market,
        "location": location,
        "results": unique_results[:10],
    }, ensure_ascii=False)
