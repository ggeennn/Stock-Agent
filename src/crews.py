# src/crews.py

from crewai import Crew, Process
from src.agents import FinancialAnalysisCrewAgents
from src.tasks import StockAnalysisTasks
from src.tools.custom_tools import IPOCalendarTool
from datetime import datetime, timedelta

class FinancialAnalysisCrew:
    def __init__(self, llm):
        self.llm = llm
        self.agents = FinancialAnalysisCrewAgents()
        self.tasks = StockAnalysisTasks()
        self.ipo_calendar_tool = IPOCalendarTool()

    def run(self):
        """
        运行一个确定性的、两阶段的工作流。
        """
        # =================================================================
        # 阶段一：确定性的数据获取 (无AI参与)
        # =================================================================
        print("\n--- [阶段一]: 正在直接执行工具以获取IPO数据 ---")
        today = datetime.now()
        end_date = (today + timedelta(days=90)).strftime("%Y-%m-%d")
        start_date = today.strftime("%Y-%m-%d")

        ipo_data = self.ipo_calendar_tool._run(
            from_date=start_date,
            to_date=end_date
        )
        print("✅ [阶段一]: 数据获取成功！")

        if "error" in ipo_data:
            print(f"❌ 工具返回错误: {ipo_data['error']}")
            return

        # =================================================================
        # 阶段二：AI驱动的报告生成
        # =================================================================
        print("\n--- [阶段二]: 正在组建AI报告团队 ---")

        # 实例化我们真正需要的报告分析师
        report_synthesizer_agent = self.agents.financial_report_synthesizer(self.llm)

        # 创建报告任务，并将正确的智能体和获取到的数据传入
        reporting_task = self.tasks.ipo_reporting_task(
            agent=report_synthesizer_agent,
            ipo_data=ipo_data
        )

        # 组建一个只包含报告智能体和报告任务的高效Crew
        crew = Crew(
            agents=[report_synthesizer_agent],
            tasks=[reporting_task],
            process=Process.sequential,
            verbose=True,
            manager_llm=self.llm
        )

        print("\n## 正在启动报告生成任务...")
        result = crew.kickoff()
        return result