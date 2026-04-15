from __future__ import annotations

from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (compatible; lilbro-research-bot/1.0)"


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
        items.append(
            {
                "title": title_el.get_text(" ", strip=True),
                "url": title_el.get("href", ""),
                "snippet": snippet_el.get_text(" ", strip=True) if snippet_el else "",
            }
        )
        if len(items) >= limit:
            break
    return items
