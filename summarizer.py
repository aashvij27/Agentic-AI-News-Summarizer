from __future__ import annotations

from typing import Any, Dict, List

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from utils import build_chat_model, clip_text


def summarize_articles(state: Dict[str, Any]) -> Dict[str, List[Dict[str, str]]]:
    llm = build_chat_model()
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a precise news analyst. Summarize the article in 4-6 bullet-free sentences. "
                "Focus on the main event, important context, and likely impact.",
            ),
            (
                "human",
                "Title: {title}\n"
                "Source: {source_name}\n"
                "Published at: {published_at}\n"
                "Article text:\n{content}",
            ),
        ]
    )
    chain = prompt | llm | StrOutputParser()

    summaries: List[Dict[str, str]] = []
    for article in state.get("retrieved_articles", []):
        summary = chain.invoke(
            {
                "title": article["title"],
                "source_name": article["source_name"],
                "published_at": article["published_at"],
                "content": clip_text(article.get("content", ""), limit=7000),
            }
        )
        summaries.append({**article, "summary": summary.strip()})

    return {"summaries": summaries}


def build_final_digest(state: Dict[str, Any]) -> Dict[str, str]:
    llm = build_chat_model()
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are producing a short daily-style news digest. Write a crisp overview with: "
                "1) a one-paragraph executive summary, and 2) a short 'Key themes' section.",
            ),
            (
                "human",
                "User query: {query}\n\nSummaries:\n{summaries_block}",
            ),
        ]
    )
    chain = prompt | llm | StrOutputParser()

    summaries_block = "\n\n".join(
        f"Title: {item['title']}\nSource: {item['source_name']}\nSummary: {item['summary']}"
        for item in state.get("summaries", [])
    )
    final_digest = chain.invoke(
        {
            "query": state.get("query", "artificial intelligence"),
            "summaries_block": summaries_block or "No summaries were generated.",
        }
    )
    return {"final_digest": final_digest.strip()}
