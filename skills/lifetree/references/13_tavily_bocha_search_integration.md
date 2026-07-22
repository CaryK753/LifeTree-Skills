# Tavily & Bocha Web Search Integration Engine

## 1. Overview
To ensure data freshness and accurate temporal knowledge graph building, LifeTree integrates advanced web search APIs via `scripts/search_connector_tavily.py`:
- **Tavily Search API**: High-precision AI web search supporting site-specific domain filtering (`include_domains`/`exclude_domains`), search depth control (`advanced`), and structured entity extraction.
- **Tavily Content Extract API (`/extract`)**: Direct full-text webpage crawling and HTML scraping endpoint.
- **Bocha (博查) Search API**: Chinese & global web search engine with summary extraction.

---

## 2. API Key Configuration
Configure API keys via environment variables or local execution parameters:
- `TAVILY_API_KEY`: API Key for Tavily Search and `/extract` endpoint.
- `BOCHA_API_KEY`: API Key for Bocha (博查) Search API.

```bash
export TAVILY_API_KEY="tvly-YOUR_KEY_HERE"
export BOCHA_API_KEY="bocha-YOUR_KEY_HERE"
```

---

## 3. Search & JIT Ingestion Pipeline
When the Agent requires real-time facts or site-specific statutory verification:
1. Execute search query with domain constraints (e.g. `include_domains: ["make-it-in-germany.com", "gesetze-im-internet.de"]`).
2. Run `scripts/search_connector_tavily.py` to retrieve structured facts or scrape full webpage content via `/extract`.
3. Pass search output into `convert_search_results_to_jit_input()` and feed directly to `scripts/jit_connector_synthesizer.py`.
4. Emit validated GraphRAG Node/Edge payloads with `Source_ID` and ISO `Valid_Time`.
