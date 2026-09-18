# digest.py
import os
from datetime import date
from core.llm import ask
from core.fetcher import fetch_news
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
MAX_ITEMS = 8          # 只取前 8 条，控制 token


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


def build_prompt(entries):
    """把新闻拼成给模型的输入"""
    lines = []
    for i, e in enumerate(entries, 1):
        summary = e.get("summary", "")[:200]   # 每条摘要截断，控制长度
        lines.append(f"{i}. 标题: {e.title}\n   摘要: {summary}")
    news_text = "\n".join(lines)
    return (
        "下面是一批新闻的标题和摘要，请用中文总结成一份简明早报，"
        "分点列出最重要的 3-5 条，每条一句话，最后给一句总体判断。\n\n"
        f"{news_text}"
    )

# new ：新增一个存文档的功能
def save_digest(text, usage):
    """把早报存成 markdown，一天一个文件"""
    os.makedirs("digests", exist_ok=True)
    today = date.today().isoformat()          # 例如 2026-09-18
    path = f"digests/{today}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# 每日早报 {today}\n\n")
        f.write(text)
        f.write(f"\n\n---\n<!-- token: {usage.total_tokens} -->\n")
    return path

def main():
    feed = fetch_news(RSS_URL)
    entries = feed.entries[:MAX_ITEMS]

    # 输出新闻内容，对比总结和获取的新闻是否对应，避免出现误差
    print("频道标题:", feed.feed.get("title"))
    print("新闻条数:", len(feed.entries))
    print("=" * 50)

    #  打印前8条
    for entry in feed.entries[:8]:
        print("标题:", entry.title)
        print("链接:", entry.link)
        print("时间:", entry.get("published", "无"))
        print("摘要:", entry.get("summary", "无摘要"))
        print("-" * 50)

    print(f"抓到 {len(feed.entries)} 条，取前 {len(entries)} 条\n")

    prompt = build_prompt(entries)
    text, usage = ask(prompt, system="你是一个专业的财经资讯编辑。")

    # response = client.chat.completions.create(
    #     model="deepseek-chat",
    #     messages=[
    #         {"role": "system", "content": "你是一个专业的财经资讯编辑。"},
    #         {"role": "user", "content": prompt},
    #     ],
    # )

    print("===== 早报 =====")
    print(text)

    path = save_digest(text, usage)
    print(f"\n已保存到：{path}")
    # print("\n===== Token 用量 =====")
    print(f"Token: {usage.total_tokens}")


if __name__ == "__main__":
    main()
