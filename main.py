# main.py
import os
from dotenv import load_dotenv
from langchain_community.chat_models.litellm import ChatLiteLLM
from datetime import datetime, timedelta
import json

# 导入我们的组件
from src.tools.custom_tools import IPOCalendarTool
from src.crews import FinancialAnalysisCrew

def main():
    load_dotenv()

    # =================================================================
    # 阶段一：确定性的数据获取 (无AI参与)
    # =================================================================
    print("--- 阶段一: 正在直接执行工具以获取IPO数据 ---")
    try:
        ipo_tool = IPOCalendarTool()
        today = datetime.now()
        ninety_days_from_now = today + timedelta(days=90)
        start_date = today.strftime("%Y-%m-%d")
        end_date = ninety_days_from_now.strftime("%Y-%m-%d")

        tool_output_dict = ipo_tool._run(from_date=start_date, to_date=end_date)
        
        if "error" in tool_output_dict:
            print(f"❌ 数据获取失败: {tool_output_dict['error']}")
            return # 如果数据获取失败，则提前退出
        
        print("✅ 数据获取成功！")
        print("------------------------------------------------\n")
    except Exception as e:
        print(f"❌ 执行工具时发生未知错误: {e}")
        return

    # =================================================================
    # 阶段二：AI驱动的报告生成
    # =================================================================
    print("--- 阶段二: 正在组建AI报告团队 ---")
    
    llm = ChatLiteLLM(
        model="gemini/gemini-2.0-flash",
        api_key=os.environ.get("GOOGLE_API_KEY"),
        # model="groq/llama3-8b-8192",
        # api_key=os.environ.get("GROQ_API_KEY"),
        temperature=0.0
    )

    # 将第一阶段获取的数据，作为输入来创建报告Crew
    financial_crew = FinancialAnalysisCrew(llm).setup_reporting_crew(tool_output_dict)
    
    print("\n## 正在启动报告生成任务...")
    result = financial_crew.kickoff()

    print("\n\n##################################################")
    print("## 团队执行完成!")
    print("## 最终报告:")
    print(result)
    print("##################################################")

if __name__ == "__main__":
    main()