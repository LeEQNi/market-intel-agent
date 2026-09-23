# query.py
import os
from dotenv import load_dotenv
from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
# 这里必须要用新版的OpenAILike才能使用别的模型，不然只能用openai
from llama_index.llms.openai_like import OpenAILike

load_dotenv()
Settings.embed_model = OllamaEmbedding(model_name="bge-m3")
Settings.llm = OpenAILike(
    model="deepseek-v4-flash",
    api_base="https://api.deepseek.com/v1",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    context_window=128000, # 关键，手动指定上下窗口，绕过模型名校验
    is_chat_model=True, # deepseek是对话模型，开启
)

# 加载已建好的索引
storage_context = StorageContext.from_defaults(persist_dir="storage")
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine()

# 问它！
questions = [
    "最近关于DeepSeek的新闻有哪些？",
    "今天市场上有哪些政策相关的消息？",
]
for q in questions:
    print(f"\n❓ {q}")
    resp = query_engine.query(q)
    print(f"💡 {resp}")
