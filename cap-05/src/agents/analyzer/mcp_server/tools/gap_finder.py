# src/agents/analyzer/mcp_server/tools/gap_finder.py
import json


def identify_market_gaps(
    competitors_json: str,
    target_market: str,
    target_location: str = "Brasil",
) -> str:
    """
    Identifica gaps de mercado baseado nos concorrentes analisados.

    Analisa padroes nos diferenciadores para identificar o que NENHUM player oferece.
    Input: JSON array de concorrentes com differentiator e market_presence
    Output: JSON com gaps identificados e oportunidade estimada
    """
    competitors = json.loads(competitors_json)

    if not isinstance(competitors, list):
        return json.dumps({"error": "Input deve ser uma lista JSON de concorrentes"})

    # Extrair todos os diferenciadores para analise de cobertura
    differentiators = [c.get("differentiator", "").lower() for c in competitors]

    # Gaps comuns em mercados de software B2B no Brasil
    potential_gaps = [
        {
            "gap": f"Interface e suporte em portugues nativo para {target_market}",
            "covered": any("portugu" in d or "brasil" in d for d in differentiators),
            "opportunity": "alta",
        },
        {
            "gap": f"Integracao com sistema fiscal brasileiro (NFe, SPED) para {target_market}",
            "covered": any("fiscal" in d or "nfe" in d or "contab" in d for d in differentiators),
            "opportunity": "media",
        },
        {
            "gap": f"Plano acessivel para PMEs com menos de 10 usuarios em {target_location}",
            "covered": any("pme" in d or "pequen" in d or "freemium" in d for d in differentiators),
            "opportunity": "alta",
        },
        {
            "gap": f"Treinamento e onboarding em portugues para {target_market}",
            "covered": any("treinament" in d or "onboard" in d for d in differentiators),
            "opportunity": "media",
        },
    ]

    # Filtrar apenas os gaps nao cobertos
    uncovered_gaps = [g for g in potential_gaps if not g["covered"]]

    return json.dumps({
        "target_market": target_market,
        "target_location": target_location,
        "gaps_identified": uncovered_gaps[:3],  # top 3 gaps
        "total_competitors_analyzed": len(competitors),
    }, ensure_ascii=False)


def recommend_positioning(
    scored_competitors_json: str,
    market_gaps_json: str,
) -> str:
    """
    Gera recomendacao de posicionamento baseada nos scores e nos gaps identificados.

    Combina analise de ameacas (scored_competitors) com oportunidades (market_gaps)
    para sugerir onde uma nova entrada tem mais chances de sucesso.
    """
    scored_data = json.loads(scored_competitors_json)
    gaps_data = json.loads(market_gaps_json)

    scored = scored_data.get("scored_competitors", [])
    gaps = gaps_data.get("gaps_identified", [])

    # Identificar o gap de maior oportunidade
    high_opp_gaps = [g for g in gaps if g.get("opportunity") == "alta"]
    main_gap = high_opp_gaps[0]["gap"] if high_opp_gaps else (gaps[0]["gap"] if gaps else "nicho nao identificado")

    # Identificar players de alta ameaca a evitar confronto direto
    high_threat = [c["name"] for c in scored if c.get("threat_level") == "alta"]

    positioning = (
        f"Focar em: {main_gap}. "
        f"Evitar confronto direto com: {', '.join(high_threat[:2]) if high_threat else 'nenhum player dominante identificado'}. "
        f"Diferencial central: solucao especializada para o gap identificado, com foco em {gaps_data.get('target_location', 'Brasil')}."
    )

    return json.dumps({
        "recommended_positioning": positioning,
        "primary_gap_opportunity": main_gap,
        "high_threat_competitors": high_threat,
        "confidence": 0.70 if len(scored) >= 3 else 0.45,
    }, ensure_ascii=False)
