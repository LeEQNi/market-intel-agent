# build_index.py
import os
from dotenv import load_dotenv
from llama_index.core import (
    VectorStoreIndex, SimpleDirectoryReader, Settings,
)
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.openai import OpenAI

load_dotenv()

# ① 嵌入模型：本地 Ollama（把文字变成向量）
Settings.embed_model = OllamaEmbedding(model_name="bge-m3")

# ② LLM：DeepSeek（负责最后"根据检索内容作答"）
Settings.llm = OpenAI(
    model="deepseek-chat",
    api_base="https://api.deepseek.com/v1",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)

# ③ 读语料 → 建索引 → 持久化到磁盘
print("读取语料中...")
documents = SimpleDirectoryReader("corpus").load_data()
print(f"共 {len(documents)} 篇文档")

print("建索引中（首次较慢）...")
index = VectorStoreIndex.from_documents(documents)

index.storage_context.persist(persist_dir="storage")
print("✅ 索引已保存到 storage/")
