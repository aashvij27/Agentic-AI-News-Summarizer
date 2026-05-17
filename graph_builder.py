from typing import List, TypedDict

from langgraph.graph import END, StateGraph

from scraper import fetch_article_bodies, fetch_news_metadata
from summarizer import build_final_digest, summarize_articles


class ArticleMetadata(TypedDict):
    title: str
    url: str
    source_name: str
    published_at: str
    description: str


class RetrievedArticle(ArticleMetadata):
    content: str


class ArticleSummary(ArticleMetadata):
    summary: str


class NewsSummarizerState(TypedDict, total=False):
    query: str
    max_articles: int
    articles: List[ArticleMetadata]
    retrieved_articles: List[RetrievedArticle]
    summaries: List[ArticleSummary]
    final_digest: str


def build_news_graph():
    graph = StateGraph(NewsSummarizerState)

    graph.add_node("fetch_news", fetch_news_metadata)
    graph.add_node("fetch_article_bodies", fetch_article_bodies)
    graph.add_node("summarize_articles", summarize_articles)
    graph.add_node("build_final_digest", build_final_digest)

    graph.set_entry_point("fetch_news")
    graph.add_edge("fetch_news", "fetch_article_bodies")
    graph.add_edge("fetch_article_bodies", "summarize_articles")
    graph.add_edge("summarize_articles", "build_final_digest")
    graph.add_edge("build_final_digest", END)

    return graph.compile()
