"""
SerpApi Service for REALITYCHECK AI
Wrapper around SerpApi Google Search SDK to fetch real-time live web search results.
"""

import os
import urllib.parse
from typing import List, Dict, Any, Optional
from serpapi import GoogleSearch
from config import get_serpapi_key

class SerpApiService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = get_serpapi_key(api_key)

    def is_configured() -> bool:
        """Check if SerpApi key is set."""
        key = get_serpapi_key()
        return bool(key and key.strip() and key != "your_serpapi_key_here")

    def search_google(self, query: str, num_results: int = 10, engine: str = "google") -> Dict[str, Any]:
        """
        Execute a live search using SerpApi Google Search API.
        
        Returns structured dictionary containing results or error message.
        """
        api_key = self.api_key or get_serpapi_key()
        if not api_key or api_key == "your_serpapi_key_here":
            return {
                "success": False,
                "error": "SerpApi key is missing. Please set SERPAPI_KEY in .env or Sidebar Settings.",
                "results": [],
                "query": query
            }

        params = {
            "engine": engine,
            "q": query,
            "api_key": api_key,
            "num": num_results,
            "gl": "us",
            "hl": "en"
        }

        try:
            search = GoogleSearch(params)
            dict_results = search.get_dict()

            # Check for API error response from SerpApi
            if "error" in dict_results:
                err_msg = dict_results["error"]
                if "Invalid API key" in err_msg or "Invalid key" in err_msg:
                    return {
                        "success": False,
                        "error": "Invalid SerpApi key provided. Please verify your SerpApi credentials.",
                        "results": [],
                        "query": query
                    }
                return {
                    "success": False,
                    "error": f"SerpApi Error: {err_msg}",
                    "results": [],
                    "query": query
                }

            # Parse search results
            parsed_items = self._parse_serp_response(dict_results)

            return {
                "success": True,
                "results": parsed_items,
                "raw_response": dict_results,
                "query": query,
                "total_results": len(parsed_items)
            }

        except Exception as e:
            err_str = str(e)
            if "HTTPError" in err_str or "401" in err_str:
                error_desc = "Authentication failed with SerpApi. Check your SERPAPI_KEY."
            elif "429" in err_str or "rate limit" in err_str.lower():
                error_desc = "SerpApi rate limit exceeded. Please try again in a few moments."
            elif "ConnectionError" in err_str or "Timeout" in err_str:
                error_desc = "Network error connecting to SerpApi. Please check internet connection."
            else:
                error_desc = f"Search execution failed: {err_str}"

            return {
                "success": False,
                "error": error_desc,
                "results": [],
                "query": query
            }

    def execute_multi_search(self, queries: List[str], max_per_query: int = 7) -> List[Dict[str, Any]]:
        """
        Execute multiple search queries (e.g. main search + counter-evidence search)
        and merge deduplicated evidence.
        """
        all_results = []
        seen_urls = set()

        for q in queries:
            search_res = self.search_google(q, num_results=max_per_query)
            if search_res.get("success"):
                for item in search_res.get("results", []):
                    url = item.get("link", "").strip()
                    # Deduplicate based on URL normalizing
                    normalized_url = url.rstrip("/").lower()
                    if normalized_url and normalized_url not in seen_urls:
                        seen_urls.add(normalized_url)
                        item["origin_query"] = q
                        all_results.append(item)

        return all_results

    def _parse_serp_response(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract structured evidence items from organic results, answer box, top news, and knowledge graph.
        """
        parsed = []

        # 1. Answer box / Direct snippet
        if "answer_box" in response:
            ab = response["answer_box"]
            snippet = ab.get("snippet") or ab.get("answer") or ab.get("result") or ""
            link = ab.get("link") or ab.get("displayed_link") or ""
            title = ab.get("title") or "Direct Answer Box"
            if snippet:
                parsed.append({
                    "title": title,
                    "link": link,
                    "snippet": snippet,
                    "source": self._extract_domain(link) if link else "Search Answer Box",
                    "domain": self._extract_domain(link),
                    "date": ab.get("date", ""),
                    "result_type": "Answer Box",
                    "position": 0
                })

        # 2. Organic results
        organic = response.get("organic_results", [])
        for idx, item in enumerate(organic, start=1):
            title = item.get("title", "")
            link = item.get("link", "")
            snippet = item.get("snippet", "") or item.get("snippet_highlighted_words", "")
            if isinstance(snippet, list):
                snippet = " ".join(snippet)
            date = item.get("date", "")
            displayed_link = item.get("displayed_link", "")
            source_name = item.get("source", "") or self._extract_domain(link or displayed_link)

            if title and link:
                parsed.append({
                    "title": title,
                    "link": link,
                    "snippet": snippet,
                    "source": source_name,
                    "domain": self._extract_domain(link),
                    "date": date,
                    "result_type": "Organic Search",
                    "position": idx
                })

        # 3. Top news / Recent news
        top_news = response.get("top_stories", []) or response.get("news_results", [])
        for idx, news in enumerate(top_news, start=100):
            title = news.get("title", "")
            link = news.get("link", "")
            snippet = news.get("snippet", "") or news.get("date", "")
            source_name = news.get("source", "") or self._extract_domain(link)
            if title and link:
                parsed.append({
                    "title": title,
                    "link": link,
                    "snippet": snippet,
                    "source": source_name,
                    "domain": self._extract_domain(link),
                    "date": news.get("date", ""),
                    "result_type": "Top Story",
                    "position": idx
                })

        return parsed

    def _extract_domain(self, url: str) -> str:
        """Extract clean domain name from URL."""
        if not url:
            return "Unknown Source"
        try:
            parsed = urllib.parse.urlparse(url)
            domain = parsed.netloc or parsed.path
            if domain.startswith("www."):
                domain = domain[4:]
            return domain
        except Exception:
            return "Web Source"
