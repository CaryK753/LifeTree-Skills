#!/usr/bin/env python3
"""
LifeTree Search Connector for Tavily & Bocha APIs
Integrates Tavily Advanced Web Search, Domain Filtering, Web Extract (/extract), and Bocha Search into JIT GraphRAG payload
"""

import os
import sys
import json
import urllib.request
import urllib.parse
from typing import Dict, Any, List, Optional

TAVILY_API_KEY_ENV = "TAVILY_API_KEY"
BOCHA_API_KEY_ENV = "BOCHA_API_KEY"

def tavily_search(query: str, api_key: Optional[str] = None, include_domains: List[str] = None, exclude_domains: List[str] = None, search_depth: str = "advanced", max_results: int = 5) -> Dict[str, Any]:
    """
    Executes a web search via Tavily API with domain filtering and structured result extraction.
    """
    key = api_key or os.getenv(TAVILY_API_KEY_ENV)
    if not key:
        return {
            "error": "MISSING_API_KEY",
            "message": f"Tavily API key not found. Set environment variable '{TAVILY_API_KEY_ENV}' or pass api_key parameter."
        }

    url = "https://api.tavily.com/search"
    payload = {
        "api_key": key,
        "query": query,
        "search_depth": search_depth,
        "include_images": False,
        "include_answer": True,
        "max_results": max_results
    }
    if include_domains:
        payload["include_domains"] = include_domains
    if exclude_domains:
        payload["exclude_domains"] = exclude_domains

    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            res_json = json.loads(resp.read().decode("utf-8"))
            return {
                "source": "TAVILY",
                "query": query,
                "answer": res_json.get("answer"),
                "results": res_json.get("results", [])
            }
    except Exception as e:
        return {"error": "API_CALL_FAILED", "message": str(e)}

def tavily_extract(urls: List[str], api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Extracts raw webpage content from specific URLs using Tavily /extract API endpoint.
    """
    key = api_key or os.getenv(TAVILY_API_KEY_ENV)
    if not key:
        return {
            "error": "MISSING_API_KEY",
            "message": f"Tavily API key not found. Set environment variable '{TAVILY_API_KEY_ENV}'."
        }

    url = "https://api.tavily.com/extract"
    payload = {
        "api_key": key,
        "urls": urls
    }
    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            res_json = json.loads(resp.read().decode("utf-8"))
            return {
                "source": "TAVILY_EXTRACT",
                "extracted": res_json.get("results", [])
            }
    except Exception as e:
        return {"error": "EXTRACT_FAILED", "message": str(e)}

def bocha_search(query: str, api_key: Optional[str] = None, count: int = 5) -> Dict[str, Any]:
    """
    Executes a web search via Bocha (博查) Search API.
    """
    key = api_key or os.getenv(BOCHA_API_KEY_ENV)
    if not key:
        return {
            "error": "MISSING_API_KEY",
            "message": f"Bocha API key not found. Set environment variable '{BOCHA_API_KEY_ENV}'."
        }

    url = "https://api.bochaai.com/v1/web-search"
    payload = {
        "query": query,
        "freshness": "noLimit",
        "summary": True,
        "count": count
    }
    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, 
        data=data_bytes, 
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            res_json = json.loads(resp.read().decode("utf-8"))
            return {
                "source": "BOCHA",
                "query": query,
                "results": res_json.get("data", {}).get("webPages", {}).get("value", [])
            }
    except Exception as e:
        return {"error": "BOCHA_CALL_FAILED", "message": str(e)}

def convert_search_results_to_jit_input(search_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converts search/extract output from Tavily or Bocha into LifeTree JIT Connector Input format
    ready for 'scripts/jit_connector_synthesizer.py'.
    """
    results = search_output.get("results", [])
    extracted = search_output.get("extracted", [])

    raw_entities = []
    source_url = "https://tavily.com/results"

    if results:
        source_url = results[0].get("url", source_url)
        for r in results:
            raw_entities.append({
                "label": r.get("title", "Search Fact"),
                "type": "POLICY_LAW",
                "snippet": r.get("content", "")[:200]
            })
    elif extracted:
        source_url = extracted[0].get("url", source_url)
        for ex in extracted:
            raw_entities.append({
                "label": f"Extracted Content: {ex.get('url')}",
                "type": "POLICY_LAW",
                "snippet": ex.get("raw_content", "")[:300]
            })

    return {
        "source_url": source_url,
        "source_type": "OFFICIAL_GAZETTE" if ".gov" in source_url or "gesetze" in source_url else "COMMUNITY_FORUM",
        "valid_start": None,
        "valid_end": None,
        "raw_entities": raw_entities,
        "raw_relations": []
    }

def main():
    if len(sys.argv) > 1:
        query = sys.argv[1]
        print(f"Testing Tavily search mock for query: '{query}'...")
    else:
        query = "Germany Chancenkarte statutory rules 2024"

    # Simulated fallback response when API keys are not provided
    mock_res = {
        "source": "TAVILY",
        "query": query,
        "answer": "Chancenkarte is effective June 1, 2024, requiring 6 points.",
        "results": [
            {
                "title": "Chancenkarte Points & Financial Requirements",
                "url": "https://www.make-it-in-germany.com/en/visa-residence/types/opportunity-card",
                "content": "The opportunity card requires 6 points and a statutory blocked account proof of €12,000 per year."
            }
        ]
    }
    
    jit_input = convert_search_results_to_jit_input(mock_res)
    print(json.dumps({
        "search_response_sample": mock_res,
        "converted_jit_input": jit_input
    }, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
