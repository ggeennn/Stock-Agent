# src/crews.py

from crewai import Crew, Process
from src.agents import FinancialAnalysisCrewAgents
from src.tasks import StockAnalysisTasks

class FinancialAnalysisCrew:
    def __init__(self, llm):
        self.llm = llm
        self.agents = FinancialAnalysisCrewAgents()
        self.tasks = StockAnalysisTasks()

    def setup_crew(self):
        # 创建智能体实例
        ipo_scout_agent = self.agents.ipo_scout(self.llm)
        # macro_analyst_agent = self.agents.macroeconomic_analyst(self.llm) # 为下一步准备

        # 1. 创建数据采集任务
        ipo_data_task = self.tasks.ipo_data_gathering_task(ipo_scout_agent)
        
        # 2. 创建报告生成任务，并将第一个任务作为其上下文
        #    这确保了报告任务只能看到工具的真实输出
        ipo_report_task = self.tasks.ipo_report_generation_task(
            agent=ipo_scout_agent, 
            context=[ipo_data_task] # 关键：将任务一作为任务二的上下文
        )
        # macro_analysis_task = self.tasks.macro_analysis_task(macro_analyst_agent) # 为下一步准备

        # 注意：在v2.0的实现中，我们将工具直接在agent定义时赋予，
        # 因此在创建Task时不再需要手动指定tools列表。
        # 这比我们之前的实现更清晰。

        # 创建并返回包含当前阶段所有智能体和任务的Crew
        return Crew(
            agents=[
                ipo_scout_agent, 
                # macro_analyst_agent # 为下一步准备
            ],
            tasks=[
                ipo_data_task,
                ipo_report_task
                # macro_analysis_task # 为下一步准备
            ],
            process=Process.sequential,
            verbose=True,
            manager_llm=self.llm
        )