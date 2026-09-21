# core/fetcher.py
import time
import requests
import feedparser

# feedparser也能指定UA
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def _fetch_raw(url, retries=3):
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            resp.raise_for_status()
            return feedparser.parse(resp.content)
        except Exception as e:
            wait = 2 ** attempt
            print(f"第 {attempt + 1} 次失败: {e}，{wait}s 后重试")
            time.sleep(wait)
    raise RuntimeError("抓取失败，已重试多次")


def fetch_rss_news(url, limit=10, source="rss"):
    """抓 RSS → 统一结构列表（和 akshare_fetcher 保持同一形状）"""
    feed = _fetch_raw(url)
    items = []
    for e in feed.entries[:limit]:
        content = e.get("summary", "")
        items.append({
            "title": e.get("title", "").strip(),
            "content": content,
            "time": e.get("published", ""),
            "source": source,
            "url": e.get("link", ""),
        })
    return items