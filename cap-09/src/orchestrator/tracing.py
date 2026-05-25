# src/orchestrator/tracing.py
import os
from langfuse.callback import CallbackHandler


def get_langfuse_handler(
    session_id: str = None,
    user_id: str = None,
    trace_name: str = "market-intelligence-run",
) -> CallbackHandler:
    """
    Cria um handler Langfuse configurado para o sistema multi-agente.

    O handler captura automaticamente:
    - Cada invocacao de LLM (tokens, latencia, modelo)
    - Cada chamada de ferramenta (nome, input, output)
    - Cada no LangGraph (inicio, fim, estado)
    """
    handler = CallbackHandler(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        host=os.getenv("LANGFUSE_HOST", "http://localhost:3000"),
        session_id=session_id,
        user_id=user_id,
        trace_name=trace_name,
    )

    return handler


def get_run_config(query: str = None) -> dict:
    """
    Retorna a configuracao de run para o graph.invoke().
    Inclui o callback handler Langfuse e metadados de rastreamento.
    """
    import hashlib
    from datetime import datetime

    # Session ID unico por execucao
    session_id = hashlib.md5(
        f"{query or 'unknown'}-{datetime.now().isoformat()}".encode()
    ).hexdigest()[:12]

    handler = get_langfuse_handler(
        session_id=session_id,
        trace_name=f"mis-run-{session_id}",
    )

    return {
        "callbacks": [handler],
        "metadata": {
            "query": query,
            "session_id": session_id,
        }
    }
