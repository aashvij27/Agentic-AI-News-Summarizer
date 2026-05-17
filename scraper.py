from __future__ import annotations

from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup

from utils import clean_text, get_news_api_key, safe_int

NEWS_API_BASE_URL = "https://newsapi.org/v2/everything"
REQUEST_TIMEOUT_SECONDS = 20


def fetch_news_metadata(state: Dict[str, Any]) -> Dict[str, List[Dict[str, str]]]:
    query = state.get("query", "artificial intelligence")
    max_articles = safe_int(state.get("max_articles", 5), default=5)
    params = {
        "q": query,
        "pageSize": max_articles,
        "sortBy": "publishedAt",
        "language": "en",
        "apiKey": get_news_api_key(),
    }

    response = requests.get(
        NEWS_API_BASE_URL,
        params=params,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    payload = response.json()

    if payload.get("status") != "ok":
        raise RuntimeError(f"NewsAPI request failed: {payload}")

    articles: List[Dict[str, str]] = []
    for article in payload.get("articles", [])[:max_articles]:
        if not article.get("url") or not article.get("title"):
            continue

        articles.append(
            {
                "title": clean_text(article.get("title", "Untitled article")),
                "url": article["url"],
                "source_name": clean_text(article.get("source", {}).get("name", "Unknown")),
                "published_at": article.get("publishedAt", "Unknown"),
                "description": clean_text(article.get("description", "")),
            }
        )

    return {"articles": articles}


def fetch_article_bodies(state: Dict[str, Any]) -> Dict[str, List[Dict[str, str]]]:
    retrieved_articles: List[Dict[str, str]] = []

    for article in state.get("articles", []):
        article_text = _scrape_article_text(article["url"])
        retrieved_articles.append(
            {
                **article,
                "content": article_text or article.get("description", ""),
            }
        )

    return {"retrieved_articles": retrieved_articles}


def _scrape_article_text(url: str) -> str:
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.RequestException:
        return ""

    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    joined = " ".join(paragraphs)
    return clean_text(joined)
