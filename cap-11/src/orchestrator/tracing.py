# src/orchestrator/tracing.py
import os
import hashlib
from datetime import datetime

# langfuse v3+: o import correto e langfuse.langchain
# langfuse v2 usava langfuse.callback (removido na v3)
from langfuse.langchain import CallbackHandler


def get_langfuse_handler(trace_id: str = None) -> CallbackHandler:
    # langfuse v3+: public_key, secret_key e host via env vars
    # LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST
    trace_context = {"trace_id": trace_id} if trace_id else None
    return CallbackHandler(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        trace_context=trace_context,
    )


def get_run_config(query: str = None) -> dict:
    trace_id = hashlib.md5(
        f"{query or 'unknown'}-{datetime.now().isoformat()}".encode()
    ).hexdigest()[:12]
    handler = get_langfuse_handler(trace_id=trace_id)
    return {"callbacks": [handler], "metadata": {"query": query, "trace_id": trace_id}}
