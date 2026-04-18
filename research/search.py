from __future__ import annotations

from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (compatible; lilbro-research-bot/1.1)"


def search_duckduckgo(query: str, limit: int = 5) -> list[dict]:
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
    response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    items = []
    for result in soup.select("div.result"):
        title_el = result.select_one("a.result__a")
        snippet_el = result.select_one("a.result__snippet, .result__snippet")
        if not title_el:
            continue
        title = title_el.get_text(" ", strip=True)
        href = title_el.get("href", "")
        snippet = snippet_el.get_text(" ", strip=True) if snippet_el else ""
        if not title or not href:
            continue
        items.append({"title": title, "url": href, "snippet": snippet})
        if len(items) >= limit:
            break
    return items


def multi_search(queries: list[str], limit: int = 5) -> list[dict]:
    seen = set()
    results = []
    for query in queries:
        try:
            items = search_duckduckgo(query, limit=limit)
        except Exception:
            items = []
        for item in items:
            key = item.get("url") or item.get("title")
            if key in seen:
                continue
            seen.add(key)
            results.append(item)
            if len(results) >= limit:
                return results
    return results
