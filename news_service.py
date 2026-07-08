"""
news_service.py
----------------
Thin wrapper around NewsAPI.org (https://newsapi.org/docs).

Two endpoints are used:
  - /v2/everything      -> free-text search across many sources
  - /v2/top-headlines    -> current headlines, optionally filtered by category

Both functions return a list of plain Python dicts (already trimmed to the
fields the frontend needs) so the rest of the app never has to think about
NewsAPI's raw response shape.
"""

import requests

NEWS_API_BASE = "https://newsapi.org/v2"

VALID_CATEGORIES = {
    "business",
    "entertainment",
    "general",
    "health",
    "science",
    "sports",
    "technology",
}


class NewsAPIError(Exception):
    """Raised whenever NewsAPI returns an error or an unexpected response."""


def _normalize(raw_articles):
    articles = []
    for a in raw_articles:
        articles.append(
            {
                "title": a.get("title") or "Untitled",
                "description": a.get("description") or "",
                "content": a.get("content") or "",
                "url": a.get("url") or "",
                "urlToImage": a.get("urlToImage") or "",
                "source": (a.get("source") or {}).get("name") or "Unknown source",
                "author": a.get("author") or "Unknown author",
                "publishedAt": a.get("publishedAt") or "",
            }
        )
    return articles


def search_news(api_key, query, language="en", sort_by="publishedAt", page_size=12):
    """Free-text search across NewsAPI's 'everything' endpoint."""
    url = f"{NEWS_API_BASE}/everything"
    params = {
        "q": query,
        "language": language,
        "sortBy": sort_by,
        "pageSize": page_size,
        "apiKey": api_key,
    }

    try:
        resp = requests.get(url, params=params, timeout=15)
    except requests.RequestException as e:
        raise NewsAPIError(f"Could not reach NewsAPI: {e}")

    data = resp.json() if resp.content else {}

    if resp.status_code != 200 or data.get("status") != "ok":
        message = data.get("message", "Failed to fetch news from NewsAPI.")
        raise NewsAPIError(message)

    return _normalize(data.get("articles", []))


def top_headlines(api_key, category=None, country="us", page_size=12):
    """Fetch current top headlines, optionally filtered by category."""
    url = f"{NEWS_API_BASE}/top-headlines"
    params = {"country": country, "pageSize": page_size, "apiKey": api_key}

    if category:
        category = category.lower()
        if category in VALID_CATEGORIES:
            params["category"] = category

    try:
        resp = requests.get(url, params=params, timeout=15)
    except requests.RequestException as e:
        raise NewsAPIError(f"Could not reach NewsAPI: {e}")

    data = resp.json() if resp.content else {}

    if resp.status_code != 200 or data.get("status") != "ok":
        message = data.get("message", "Failed to fetch headlines from NewsAPI.")
        raise NewsAPIError(message)

    return _normalize(data.get("articles", []))
