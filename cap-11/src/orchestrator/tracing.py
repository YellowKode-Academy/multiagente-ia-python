# src/orchestrator/tracing.py
import os
import hashlib
from datetime import datetime
from langfuse.callback import CallbackHandler


def get_langfuse_handler(session_id: str = None, trace_name: str = "market-intelligence-run") -> CallbackHandler:
    return CallbackHandler(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        host=os.getenv("LANGFUSE_HOST", "http://localhost:3000"),
        session_id=session_id,
        trace_name=trace_name,
    )


def get_run_config(query: str = None) -> dict:
    session_id = hashlib.md5(
        f"{query or 'unknown'}-{datetime.now().isoformat()}".encode()
    ).hexdigest()[:12]
    handler = get_langfuse_handler(session_id=session_id, trace_name=f"mis-run-{session_id}")
    return {"callbacks": [handler], "metadata": {"query": query, "session_id": session_id}}
