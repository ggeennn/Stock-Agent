import os
from crewai import Crew, Process, Task # <-- 修正：直接导入Task
from dotenv import load_dotenv
from langchain_community.chat_models.litellm import ChatLiteLLM
from datetime import datetime, timedelta
from textwrap import dedent # <-- 修正：直接导入dedent

from src.agents import FinancialAnalysisCrewAgents
from src.tools.custom_tools import IPOCalendarTool

load_dotenv()

llm = ChatLiteLLM(
    model="groq/llama3-8b-8192",
    api_key=os.environ.get("GROQ_API_KEY")
)

def run_crew():
    """设置并启动金融分析Crew。"""
    
    print("======================================")
    print("## 欢迎来到GEM金融智能体 v2.0核心引擎 ##")
    print("======================================")
    
    agents = FinancialAnalysisCrewAgents()
    # tasks = StockAnalysisTasks() # <-- 我们不再需要实例化这个类
    ipo_scout_agent = agents.ipo_scout(llm=llm)
    ipo_calendar_tool = IPOCalendarTool()
    
    # --- 动态生成任务描述 ---
    today = datetime.now()
    ninety_days_from_now = today + timedelta(days=90)
    start_date = today.strftime("%Y-%m-%d")
    end_date = ninety_days_from_now.strftime("%Y-%m-%d")
    
    # --- 直接创建Task实例 ---
    ipo_discovery_task = Task(
        description=dedent(f"""
            使用你的IPO日历工具，扫描从 {start_date} 到 {end_date} 的所有即将进行的和近期已定价的首次公开募股（IPO）。
            对每一个发现的IPO，提供其公司名称、股票代码、预估的上市日期和交易所。
            将所有发现结构化地整理成一份简洁的报告。
            重要提示：你的任务只是查找IPO日历，不要去扫描新闻源。
        """),
        expected_output=dedent("""
            一份Markdown格式的报告，只包含一个部分：“近期及未来IPO列表”。
            该列表以项目符号（bullet points）的形式展示每个IPO的关键信息（公司名称、股票代码、日期、交易所）。
        """),
        agent=ipo_scout_agent,
        tools=[ipo_calendar_tool]
    )
    
    crew = Crew(
        agents=[ipo_scout_agent],
        tasks=[ipo_discovery_task],
        process=Process.sequential,
        verbose=True,
        manager_llm=llm
    )

    print(f"\n## 正在启动IPO发现任务 (日期范围: {start_date} to {end_date})...")
    result = crew.kickoff()

    print("\n\n##################################################")
    print("## 团队执行完成!")
    print("## 最终报告:")
    print(result)
    print("##################################################")

if __name__ == "__main__":
    run_crew()