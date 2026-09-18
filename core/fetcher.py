# core/fetcher.py
import time
import requests
import feedparser

# feedparser也能指定UA
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def fetch_news(url, retries=3):
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
