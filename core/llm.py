# core/llm.py
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

_client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


def ask(prompt, system="你是一个专业助手。"):
    """统一入口：发一条 user 消息，返回 (回复文字, token用量)"""
    resp = _client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        temperature=0,  # ← 关键：尽量取最确定输出
        top_p=1,  # ← 配合 temperature，去掉采样随机
    )
    return resp.choices[0].message.content, resp.usage
