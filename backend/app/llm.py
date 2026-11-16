"""Cloud LLM client (OpenAI-compatible API).

The client is ``None`` when no API key is configured; every call site already
has a local fallback reply, so the API keeps working in degraded mode.
Credentials come from ``backend/.env`` via :mod:`app.config` -- never from
source code.
"""

from openai import OpenAI

from app.config import LLM_API_KEY, LLM_BASE_URL

print("Connecting to Cloud LLM Engine...")

LLM_CLIENT = (
    OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL) if LLM_API_KEY else None
)
