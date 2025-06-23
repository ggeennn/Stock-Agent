import os
from dotenv import load_dotenv

# 从 .env 文件加载环境变量
load_dotenv()

# 从环境中获取 API 密钥
tavily_api_key = os.getenv("TAVILY_API_KEY")

# 打印结果来验证
print(f"--- 调试环境测试 ---")
if tavily_api_key:
    print(f"✅ 成功加载 TAVILY_API_KEY: '{tavily_api_key}'")
else:
    print(f"❌ 未能加载 TAVILY_API_KEY。")
print(f"--------------------")