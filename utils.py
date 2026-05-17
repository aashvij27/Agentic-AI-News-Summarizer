from __future__ import annotations

import os
import re

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def get_news_api_key() -> str:
    return get_required_env("NEWS_API_KEY")


def build_chat_model():
    provider = os.getenv("LLM_PROVIDER", "openai").strip().lower()

    if provider == "openai":
        api_key = get_required_env("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        return ChatOpenAI(model=model, api_key=api_key, temperature=0.2)

    if provider == "ollama":
        model = os.getenv("OLLAMA_MODEL", "llama3.1")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        return ChatOllama(model=model, base_url=base_url, temperature=0.2)

    raise ValueError("Unsupported LLM_PROVIDER. Use 'openai' or 'ollama'.")


def clip_text(text: str, limit: int = 7000) -> str:
    cleaned = clean_text(text)
    return cleaned[:limit]


def clean_text(text: str) -> str:
    collapsed = re.sub(r"\s+", " ", text or "").strip()
    return collapsed


def safe_int(value, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
