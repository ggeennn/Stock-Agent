# src/tasks.py
from crewai import Task
from textwrap import dedent

class StockAnalysisTasks():
    def reporting_task(self, agent, context_data):
        return Task(
            description=dedent(f"""
                分析在下面提供的IPO数据，它是一个Python字典。
                你的任务是根据这份数据，将其格式化为一份清晰、简洁的Markdown报告。
                报告应该包含一个主标题“近期及未来IPO列表”，然后将每个IPO信息作为一个列表项展示出来。
                确保报告中只包含上下文中提供的数据，不要添加任何额外信息。

                IPO DATA:
                {context_data}
            """),
            expected_output="一份格式化的Markdown报告，总结了所提供的IPO数据。",
            agent=agent
        )