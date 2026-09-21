# akshare_demo.py
import akshare as ak
import os
from datetime import date

# 列出所有以 "news" 或 "stock_news" 相关的函数名
names = [n for n in dir(ak) if "news" in n.lower() or "info" in n.lower()]
print("\n".join(names))


# 东方财富-个股新闻。参数 symbol 是股票代码
df = ak.stock_news_em(symbol="000001")   # 平安银行
print(df.head())          # 看前5行
print(df.columns)         # 看有哪些列

# 财联社电报-全球快讯（不需要参数，直接拿最新快讯）
df = ak.stock_info_global_cls(symbol="全部")
os.makedirs("data", exist_ok=True)
path = f"data/news_{date.today().isoformat()}.csv"
# encoding="utf-8-sig"：中文存 CSV 必须加这个，否则 Excel 打开会乱码。
df.to_csv(path, index=False, encoding="utf-8-sig")
print(f"已保存 {len(df)} 条到 {path}")

