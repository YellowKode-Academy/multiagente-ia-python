# src/orchestrator/api.py
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from .graph import graph
from .tracing import get_run_config

load_dotenv()

app = FastAPI(
    title="Market Intelligence System",
    description="Sistema multi-agente de inteligencia competitiva",
    version="1.0.0",
)


class AnalyzeRequest(BaseModel):
    query: str
    session_id: str = None


class AnalyzeResponse(BaseModel):
    status: str
    research_result: str = None
    analysis_result: str = None
    report: str = None
    elapsed_seconds: float = None


@app.get("/health")
async def health():
    return {"status": "ok", "service": "orchestrator"}


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    """Executa analise competitiva completa via sistema multi-agente."""

    if not request.query or len(request.query.strip()) < 5:
        raise HTTPException(status_code=400, detail="Query muito curta")

    initial_state = {
        "query": request.query,
        "research_result": None,
        "analysis_result": None,
        "report": None,
        "next": "",
        "messages": [],
        "completed_agents": [],
    }

    run_config = get_run_config(query=request.query)

    start = time.time()

    try:
        # graph.ainvoke() - versao async nativa do LangGraph
        # Os nos precisam ser async def (ver agentes abaixo)
        result = await graph.ainvoke(initial_state, config=run_config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na analise: {str(e)}")

    elapsed = time.time() - start

    return AnalyzeResponse(
        status=result.get("next", "unknown"),
        research_result=result.get("research_result"),
        analysis_result=result.get("analysis_result"),
        report=result.get("report"),
        elapsed_seconds=round(elapsed, 1),
    )
