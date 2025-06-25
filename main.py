# main.py

import os
from dotenv import load_dotenv
from langchain_community.chat_models.litellm import ChatLiteLLM
# ⬇️ 只需从新的crews模块导入主Crew类 ⬇️
from src.crews import FinancialAnalysisCrew

def main():
    load_dotenv()

    print("========================================")
    print("## 欢迎来到GEM金融智能体 v2.0核心引擎 ##")
    print("========================================")

    llm = ChatLiteLLM(
        # model="gemini/gemini-2.0-flash", 
        # api_key=os.environ.get("GEMINI_API_KEY"),
        model="groq/llama3-8b-8192", 
        api_key=os.environ.get("GROQ_API_KEY"),        
        temperature=0.0 # 确保确定性输出
    )

    # 实例化并运行Crew
    financial_crew = FinancialAnalysisCrew(llm).setup_crew()

    print("\n## 正在启动v2.0 IPO发现任务...")
    result = financial_crew.kickoff()

    print("\n\n##################################################")
    print("## 团队执行完成!")
    print("## 最终报告:")
    print(result)
    print("##################################################")

if __name__ == "__main__":
    main()