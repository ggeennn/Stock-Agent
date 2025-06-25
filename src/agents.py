# src/agents.py
from crewai import Agent

# 我们暂时不需要 FinancialTools 类，因为工具将在main.py中直接调用
# from src.tools.custom_tools import IPOCalendarTool 

class FinancialAnalysisCrewAgents():
    # IPO Scout不再需要，因为它的工作由确定性代码完成
    # def ipo_scout(self, llm): ...

    def reporting_analyst(self, llm):
        return Agent(
            role='金融报告分析师',
            goal='根据提供的数据，生成一份结构清晰、格式优美的Markdown报告。',
            backstory="你是一位注重细节的分析师，擅长将结构化数据转化为人类易于阅读的、有条理的报告。",
            tools=[], # 这个智能体只进行写作，不需要外部工具
            llm=llm,
            verbose=True,
            allow_delegation=False
        )