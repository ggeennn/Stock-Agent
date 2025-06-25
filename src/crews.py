# src/crews.py
from crewai import Crew, Process
from src.agents import FinancialAnalysisCrewAgents
from src.tasks import StockAnalysisTasks

class FinancialAnalysisCrew:
    def __init__(self, llm):
        self.llm = llm
        self.agents = FinancialAnalysisCrewAgents()
        self.tasks = StockAnalysisTasks()

    def setup_reporting_crew(self, ipo_data):
        # 创建报告智能体
        reporting_analyst_agent = self.agents.reporting_analyst(self.llm)

        # 创建报告任务，并将获取到的ipo_data作为上下文
        create_report_task = self.tasks.reporting_task(reporting_analyst_agent, ipo_data)

        # 组建只包含报告任务的Crew
        return Crew(
            agents=[reporting_analyst_agent],
            tasks=[create_report_task],
            process=Process.sequential,
            verbose=True
        )