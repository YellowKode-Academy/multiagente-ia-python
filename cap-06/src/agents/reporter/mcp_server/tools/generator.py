# src/agents/reporter/mcp_server/tools/generator.py
import json
from datetime import datetime
from pathlib import Path


def generate_executive_summary(
    analysis_json: str,
    query: str,
) -> str:
    """
    Gera o resumo executivo do relatorio de inteligencia competitiva.
    Input: JSON da analise (scored_competitors, market_gaps, recommended_positioning)
    Output: texto markdown formatado para o resumo executivo
    """
    analysis = json.loads(analysis_json)

    scored = analysis.get("scored_competitors", [])
    gaps = analysis.get("market_gaps", [])
    positioning = analysis.get("recommended_positioning", "")
    confidence = analysis.get("analysis_confidence", 0.5)

    # Identificar o concorrente mais amecador
    top_competitor = scored[0] if scored else {"name": "Nenhum identificado", "score": 0}

    # Identificar gaps de alta oportunidade
    high_opp = [g for g in gaps if g.get("opportunity") == "alta"]
    main_opportunity = high_opp[0]["gap"] if high_opp else (gaps[0]["gap"] if gaps else "A identificar")

    summary = f"""## Resumo Executivo

**Mercado analisado:** {query}
**Data:** {datetime.now().strftime('%d/%m/%Y')}
**Confianca da analise:** {int(confidence * 100)}%

### Situacao Competitiva

O mercado apresenta **{len(scored)} players identificados**, com {top_competitor['name']} como principal ameaca (score: {top_competitor.get('score', 'N/A')}/100).

### Principal Oportunidade

{main_opportunity}

### Recomendacao de Posicionamento

{positioning}
"""

    return json.dumps({"summary_markdown": summary}, ensure_ascii=False)


def format_competitor_table(scored_competitors_json: str) -> str:
    """
    Formata a tabela de concorrentes em markdown.
    Input: JSON com scored_competitors
    Output: tabela markdown formatada
    """
    data = json.loads(scored_competitors_json)
    competitors = data.get("scored_competitors", [])

    if not competitors:
        return json.dumps({"table_markdown": "_Nenhum concorrente identificado._"})

    rows = []
    for c in competitors:
        threat_label = {"alta": "Alta", "media": "Media", "baixa": "Baixa"}.get(
            c.get("threat_level", "media"), "N/A"
        )
        rows.append(
            f"| {c['name']} | {c.get('score', 0)}/100 | {threat_label} |"
        )

    table = """## Analise de Concorrentes

| Concorrente | Score | Nivel de Ameaca |
|---|---|---|
""" + "\n".join(rows)

    return json.dumps({"table_markdown": table}, ensure_ascii=False)


def format_gaps_section(market_gaps_json: str) -> str:
    """
    Formata a secao de gaps de mercado em markdown.
    Input: JSON com gaps_identified
    Output: secao markdown formatada
    """
    data = json.loads(market_gaps_json)
    gaps = data.get("gaps_identified", [])

    if not gaps:
        return json.dumps({"gaps_markdown": "## Gaps de Mercado\n\n_Sem gaps identificados._"})

    items = []
    for g in gaps:
        opp_label = {"alta": "**Alta oportunidade**", "media": "Media oportunidade"}.get(
            g.get("opportunity", "media"), "Oportunidade"
        )
        items.append(f"- {g['gap']} ({opp_label})")

    section = "## Gaps de Mercado\n\n" + "\n".join(items)

    return json.dumps({"gaps_markdown": section}, ensure_ascii=False)


def export_report(
    executive_summary: str,
    competitor_table: str,
    gaps_section: str,
    output_path: str = "relatorio.md",
) -> str:
    """
    Combina todas as secoes e salva o relatorio final em markdown.
    Input: secoes individuais em markdown
    Output: path do arquivo gerado
    """
    full_report = f"""# Relatorio de Inteligencia Competitiva

{executive_summary}

---

{competitor_table}

---

{gaps_section}

---

_Relatorio gerado automaticamente pelo market-intelligence-system_
_Powered by YellowKode AI_
"""

    Path(output_path).write_text(full_report, encoding="utf-8")

    return json.dumps({
        "output_path": output_path,
        "word_count": len(full_report.split()),
        "sections": ["executive_summary", "competitor_table", "gaps_section"],
    }, ensure_ascii=False)
