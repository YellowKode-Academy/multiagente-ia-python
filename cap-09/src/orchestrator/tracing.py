# src/orchestrator/tracing.py
import os
import hashlib
from datetime import datetime

# langfuse v3+: o import correto e langfuse.langchain
# langfuse v2 usava langfuse.callback (removido na v3)
from langfuse.langchain import CallbackHandler


def get_langfuse_handler(trace_id: str = None) -> CallbackHandler:
    """
    Cria um handler Langfuse configurado para o sistema multi-agente.

    O handler captura automaticamente:
    - Cada invocacao de LLM (tokens, latencia, modelo)
    - Cada chamada de ferramenta (nome, input, output)
    - Cada no LangGraph (inicio, fim, estado)

    Nota: langfuse v3+ configura public_key, secret_key e host via
    variaveis de ambiente LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY,
    LANGFUSE_HOST. O construtor aceita apenas public_key e trace_context.
    """
    trace_context = {"trace_id": trace_id} if trace_id else None
    handler = CallbackHandler(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        trace_context=trace_context,
    )
    return handler


def get_run_config(query: str = None) -> dict:
    """
    Retorna a configuracao de run para o graph.invoke().
    Inclui o callback handler Langfuse e metadados de rastreamento.
    """
    # Session ID unico por execucao (usado como trace_id)
    trace_id = hashlib.md5(
        f"{query or 'unknown'}-{datetime.now().isoformat()}".encode()
    ).hexdigest()[:12]

    handler = get_langfuse_handler(trace_id=trace_id)

    return {
        "callbacks": [handler],
        "metadata": {
            "query": query,
            "trace_id": trace_id,
        }
    }
