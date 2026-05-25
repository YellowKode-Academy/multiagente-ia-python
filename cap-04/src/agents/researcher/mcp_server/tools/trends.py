# src/agents/researcher/mcp_server/tools/trends.py
import json
from datetime import datetime


async def get_market_trends(market: str, timeframe: str = "6 months") -> str:
    """
    Identifica tendencias recentes em um mercado especifico.
    Usa busca contextualizada para capturar mudancas recentes.
    """
    # Tendencias via busca web contextualizada
    # Em producao, pode integrar com Google Trends API
    query_parts = [
        f"tendencias {market} {datetime.now().year}",
        f"novidades {market} software Brasil",
        f"o que esta mudando {market} tecnologia",
    ]

    trends_data = {
        "market": market,
        "timeframe": timeframe,
        "query_used": query_parts[0],
        "note": "Execute search_web com os queries para dados reais",
    }

    return json.dumps(trends_data, ensure_ascii=False)
