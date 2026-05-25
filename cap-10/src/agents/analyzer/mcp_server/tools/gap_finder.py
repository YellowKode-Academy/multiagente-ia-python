# src/agents/analyzer/mcp_server/tools/gap_finder.py
# (identico ao cap-05 - copiado para manter cap-10 autocontido)
import json


def identify_market_gaps(
    competitors_json: str,
    target_market: str,
    target_location: str = "Brasil",
) -> str:
    """Identifica gaps de mercado baseado nos concorrentes analisados."""
    competitors = json.loads(competitors_json)

    if not isinstance(competitors, list):
        return json.dumps({"error": "Input deve ser uma lista JSON de concorrentes"})

    differentiators = [c.get("differentiator", "").lower() for c in competitors]

    potential_gaps = [
        {
            "gap": f"Interface e suporte em portugues nativo para {target_market}",
            "covered": any("portugu" in d or "brasil" in d for d in differentiators),
            "opportunity": "alta",
        },
        {
            "gap": f"Integracao com sistema fiscal brasileiro para {target_market}",
            "covered": any("fiscal" in d or "nfe" in d for d in differentiators),
            "opportunity": "media",
        },
        {
            "gap": f"Plano acessivel para PMEs em {target_location}",
            "covered": any("pme" in d or "pequen" in d or "freemium" in d for d in differentiators),
            "opportunity": "alta",
        },
    ]

    uncovered_gaps = [g for g in potential_gaps if not g["covered"]]

    return json.dumps({
        "target_market": target_market,
        "target_location": target_location,
        "gaps_identified": uncovered_gaps[:3],
        "total_competitors_analyzed": len(competitors),
    }, ensure_ascii=False)
