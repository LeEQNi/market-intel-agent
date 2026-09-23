# core/store.py
import os
from datetime import date

def save_corpus(items, folder="corpus"):
    """把采集的资讯存成 markdown，既是存档，也是 RAG 的语料"""
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{date.today().isoformat()}.md")
    with open(path, "w", encoding="utf-8") as f:
        for it in items:
            f.write(f"## {it['title']}\n")
            f.write(f"来源: {it['source']} | 时间: {it['time']}\n\n")
            f.write(it["content"] + "\n\n---\n\n")
    return path
