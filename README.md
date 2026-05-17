# Agentic AI News Retrieval & Summarization

An autonomous multi-agent pipeline that fetches, scrapes, and summarizes real-time news articles into a structured digest — built with **LangGraph**, **LangChain**, and **NewsAPI**.

---

## What It Does

Given a search topic, the agent automatically:

1. Queries **NewsAPI** for the latest articles on that topic
2. Scrapes full article text from each source URL
3. Summarizes each article using an LLM (4–6 sentences, no fluff)
4. Produces a final **executive digest** with key themes across all articles

---

## Architecture

The workflow is a typed **LangGraph state machine** — four nodes wired in sequence:

```
fetch_news → fetch_article_bodies → summarize_articles → build_final_digest
```

| File | Role |
|---|---|
| `main.py` | CLI entrypoint with `--query` and `--max-articles` flags |
| `graph_builder.py` | LangGraph workflow definition and state schema |
| `scraper.py` | NewsAPI fetch + BeautifulSoup article scraper |
| `summarizer.py` | Per-article LLM summarization + final digest generation |
| `utils.py` | Env config, LLM provider switching, text cleaning helpers |

---

## Tech Stack

- **LangGraph** — agentic workflow orchestration
- **LangChain** — LLM chaining and prompt management
- **NewsAPI** — real-time news retrieval
- **BeautifulSoup** — article body scraping
- **OpenAI GPT-4o-mini / Ollama (llama3.1)** — summarization LLM (switchable via `.env`)

---

## Setup

```bash
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with your keys:

```env
NEWS_API_KEY=your_newsapi_key_here

# Option 1 — OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# Option 2 — Local Ollama (free)
# LLM_PROVIDER=ollama
# OLLAMA_MODEL=llama3.1
# OLLAMA_BASE_URL=http://localhost:11434
```

Get a free NewsAPI key at [newsapi.org](https://newsapi.org).

---

## Run

```bash
python main.py --query "artificial intelligence" --max-articles 5
```

### Sample Output

```
=== News Digest ===
This week in AI saw major announcements from... [executive summary paragraph]

Key themes:
- LLM cost reductions across major providers
- Growing enterprise adoption of agentic workflows
- Regulatory developments in the EU AI Act

=== Article Summaries ===

1. OpenAI Cuts API Prices by 50%
   Source: TechCrunch
   URL: https://...
   Summary: OpenAI announced significant price reductions across its API...
```

---

## Notes

- Supports two LLM backends: **OpenAI** (cloud) or **Ollama** (local/free)
- Falls back to article description when a site blocks scraping
- All text is clipped to 7,000 chars per article before LLM processing to stay within context limits
