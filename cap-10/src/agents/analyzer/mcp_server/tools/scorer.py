# src/agents/analyzer/mcp_server/tools/scorer.py
# (identico ao cap-05 - copiado para manter cap-10 autocontido)
import json
from typing import Optional
from pydantic import BaseModel, field_validator


class CompetitorInput(BaseModel):
    name: str
    differentiator: str
    market_presence: str
    funding_stage: Optional[str] = None
    founded_year: Optional[int] = None

    @field_validator("market_presence", mode="before")
    @classmethod
    def validate_presence(cls, v):
        valid = {"alta", "media", "baixa"}
        if str(v).lower() not in valid:
            return "media"
        return str(v).lower()


def score_competitor(
    name: str,
    differentiator: str,
    market_presence: str,
    funding_stage: Optional[str] = None,
    founded_year: Optional[int] = None,
) -> str:
    """Calcula score de ameaca competitiva de 0-100."""
    presence_scores = {"alta": 40, "media": 24, "baixa": 8}
    presence_score = presence_scores.get(market_presence.lower(), 20)
    diff_score = min(30, (len(differentiator) // 5))
    maturity_score = 15
    if funding_stage:
        funding_boost = {"series_c_plus": 15, "series_b": 12, "series_a": 8, "seed": 4}.get(
            funding_stage.lower().replace(" ", "_").replace("-", "_"), 0
        )
        maturity_score = min(30, maturity_score + funding_boost)

    total_score = min(100, presence_score + diff_score + maturity_score)
    if total_score >= 70:
        threat_level = "alta"
    elif total_score >= 45:
        threat_level = "media"
    else:
        threat_level = "baixa"

    return json.dumps({
        "name": name,
        "score": total_score,
        "threat_level": threat_level,
        "score_breakdown": {
            "market_presence": presence_score,
            "differentiator_specificity": diff_score,
            "maturity": maturity_score,
        }
    }, ensure_ascii=False)


def score_competitors_batch(competitors_json: str) -> str:
    """Processa lista de concorrentes e retorna todos os scores."""
    try:
        raw_data = json.loads(competitors_json)
        if not isinstance(raw_data, list):
            raw_data = raw_data.get("competitors", [])
        competitors = [CompetitorInput(**c) for c in raw_data if isinstance(c, dict)]
    except Exception as e:
        return json.dumps({"error": f"Input invalido: {str(e)}", "scored_competitors": []})

    scored = []
    for competitor in competitors:
        result_str = score_competitor(
            name=competitor.name,
            differentiator=competitor.differentiator,
            market_presence=competitor.market_presence,
            funding_stage=competitor.funding_stage,
            founded_year=competitor.founded_year,
        )
        scored.append(json.loads(result_str))

    scored.sort(key=lambda x: x["score"], reverse=True)
    return json.dumps({"scored_competitors": scored}, ensure_ascii=False)
