# === File: test_env.py ===
import os

# 1. "索要"一个叫 "GREETING" 的便签, 兜底值是 "Hello"
my_greeting = os.getenv("GREETING", "Hello")

# 2. "索要"一个叫 "DATABASE_URL" 的便签, 兜底值是 "LOCAL_DB"
db_val = os.getenv("DATABASE_URL", "LOCAL_DB")

# 3. 打印它找到了什么
print(f"Greeting found: {my_greeting}")
print(f"Database found: {db_val}")