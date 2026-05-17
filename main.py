import argparse

from graph_builder import build_news_graph

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Retrieve news articles and build a summarized digest with LangGraph."
    )
    parser.add_argument(
        "--query",
        default="artificial intelligence",
        help="Topic to search for in the news feed.",
    )
    parser.add_argument(
        "--max-articles",
        type=int,
        default=5,
        help="Maximum number of articles to retrieve and summarize.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    graph = build_news_graph()
    result = graph.invoke({"query": args.query, "max_articles": args.max_articles})

    print("\n=== News Digest ===")
    print(result["final_digest"])
    print("\n=== Article Summaries ===")

    for index, item in enumerate(result["summaries"], start=1):
        print(f"\n{index}. {item['title']}")
        print(f"   Source: {item['source_name']}")
        print(f"   URL: {item['url']}")
        print(f"   Summary: {item['summary']}")


if __name__ == "__main__":
    main()
