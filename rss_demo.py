# rss_demo.py
import feedparser

# 1. 一个 RSS 源的地址（先用一个通用的新闻源试试）
RSS_URL = "https://www.36kr.com/feed-newsflash"

# 2. 抓取并解析
feed = feedparser.parse(RSS_URL)

# 3. 看看基本信息
print("频道标题:", feed.feed.get("title"))
print("新闻条数:", len(feed.entries))
print("=" * 50)

# 4. 逐条打印，先只看前 5 条
for entry in feed.entries[:5]:
    print("标题:", entry.title)
    print("链接:", entry.link)
    print("时间:", entry.get("published", "无"))
    print("-" * 50)