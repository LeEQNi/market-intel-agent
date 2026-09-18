# hello_llm.py
import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. 把 .env 里的变量加载到环境变量里
load_dotenv()

# 2. 创建客户端：告诉它"用哪个 key"和"连哪个服务器"
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

# 3. 发起一次对话请求
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个简洁的助手，回答不超过20字。"},
        {"role": "user", "content": "用一句话介绍你自己。"},
    ],
)

# 4. 取出模型回复的文字
print("=== 模型回复 ===")
print(response.choices[0].message.content)

# 5. 打印 token 消耗（A2 的过关标志）
print("=== Token 用量 ===")
print(response.usage)
