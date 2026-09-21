# digest.py
import os
from datetime import date
from core.llm import ask
from core.akshare_fetcher import fetch_cls_news
from core.fetcher import fetch_rss_news
# from dotenv import load_dotenv
# from openai import OpenAI

# 注释内容大多分化到llm和fetcher中
# load_dotenv()
#
# client = OpenAI(
#     api_key=os.getenv("DEEPSEEK_API_KEY"),
#     base_url="https://api.deepseek.com",
# )

# 换成你已经跑通的 RSS 地址
RSS_URL = "https://www.36kr.com/feed-newsflash"
# feedparser也能指定UA
# HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
# MAX_ITEMS = 8          # 只取前 8 条，控制 token


# def fetch_news(url, retries=3):
#     """抓 RSS，带超时 + 指数退避重试"""
#     for attempt in range(retries):
#         try:
#             resp = requests.get(url, headers=HEADERS, timeout=10)
#             resp.raise_for_status()          # 非 200 会抛异常
#             return feedparser.parse(resp.content)
#         except Exception as e:
#             wait = 2 ** attempt               # 1, 2, 4 秒
#             print(f"第 {attempt + 1} 次失败: {e}，{wait}s 后重试")
#             time.sleep(wait)
#     raise RuntimeError("抓取失败，已重试多次")

def collect_all():
    """从所有数据源采集，合并成一个统一列表"""
    items = []
    # 源1：财联社快讯
    items += fetch_cls_news(limit=15)
    # 源2：36kr RSS
    items += fetch_rss_news(RSS_URL, limit=8, source="36kr")
    return items

def build_prompt(items):
    """把新闻拼成给模型的输入"""
    lines = []
    # for i, e in enumerate(entries, 1):
    #     summary = e.get("summary", "")[:200]   # 每条摘要截断，控制长度
    #     lines.append(f"{i}. 标题: {e.title}\n   摘要: {summary}")
    #

    for i, it in enumerate(items, 1):
        content = it["content"][:150]          # 每条正文截断，控制 token
        lines.append(
            f"{i}. [{it['source']}] {it['title']}\n   {content}"
        )

    news_text = "\n".join(lines)

    return (
        # "下面是一批新闻的标题和摘要，请用中文总结成一份简明早报，"
        # "分点列出最重要的 3-5 条，每条一句话，最后给一句总体判断。\n\n"
        # f"{news_text}"
        "下面是一批财经资讯（来源已标注），请用中文总结成一份简明早报：\n"
        "1) 分点列出最重要的 3-6 条，每条一句话；\n"
        "2) 每条注明来源；\n"
        "3) 最后给一句总体判断。\n\n"
        f"{news_text}"
    )

# new ：新增一个存文档的功能
def save_digest(text, usage, count):
    """把早报存成 markdown，一天一个文件"""
    os.makedirs("digests", exist_ok=True)
    today = date.today().isoformat()          # 例如 2026-09-18
    path = f"digests/{today}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# 每日早报 {today}\n\n")
        # f.write(text)
        # f.write(f"\n\n---\n<!-- token: {usage.total_tokens} -->\n")
        f.write(f"> 数据源：cls + 36kr | 共 {count} 条 | token：{usage.total_tokens}\n\n")
        f.write(text)
    return path


def main():
    items = collect_all()
    print(f"共采集 {len(items)} 条\n")
    
    prompt = build_prompt(items)
    text, usage = ask(prompt, system="你是一个专业的财经资讯编辑。")

    print("===== 早报 =====")
    print(text)

    path = save_digest(text, usage, len(items))
    print(f"\n已保存到：{path}")
    # print("\n===== Token 用量 =====")
    print(f"Token: {usage.total_tokens}")


if __name__ == "__main__":
    main()
