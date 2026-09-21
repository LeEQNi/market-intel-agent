# core/akshare_fetcher.py
import akshare as ak

def _derive_title(content, max_len=40):
    """标题为空时，从正文截取前 max_len 字"""
    content = (content or "").strip()
    if len(content) <= max_len:
        return content
    return content[:max_len] + "..."


def fetch_cls_news(limit=20):
    """财联社全球快讯→统一结构列表"""
    df = ak.stock_info_global_cls(symbol="全部")
    items = []
    for _, row in df.head(limit).iterrows():
        title = (row.get("标题") or "").strip()
        # 清洗后的数据
        content = (row.get("内容") or "").strip()
        items.append({
            "title": title or _derive_title(content),
            "content": content,
            "time": row.get("发布时间", ""),
            "source": "cls",
            "url": "",
        })
    return items

def fetch_stock_news(symbol, limit=10):
    """个股新闻 → 统一结构列表"""
    df = ak.stock_news_em(symbol=symbol)
    items = []
    for _, row in df.head(limit).iterrows():
        title = (row.get("新闻标题") or "").strip()
        content = (row.get("新闻内容") or "").strip()
        items.append({
            "title": title or _derive_title(content),
            "content": content,
            "time": row.get("发布时间", ""),
            "source": "eastmoney",
            "url": row.get("新闻链接", ""),
        })
    return items


# 单独测试这个文件时跑
if __name__ == "__main__":
    news = fetch_cls_news(5)
    for n in news:
        print(f"[{n['source']}] {n['time']} | {n['title']}")
        print("   内容前50字:", n["content"][:50])
        print("-" * 60)