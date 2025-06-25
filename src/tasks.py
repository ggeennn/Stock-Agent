# src/tasks.py

from crewai import Task
from textwrap import dedent


class StockAnalysisTasks():
    
    def ipo_reporting_task(self, agent, ipo_data):
        """
        最终的报告任务。
        它接收已经获取到的、真实的IPO数据，并只负责撰写报告。
        """
        return Task(
            description=dedent(f"""
                分析下面提供给你的IPO数据，并撰写一份专业的Markdown报告。

                **IPO 数据:**
                ```json
                {ipo_data}
                ```

                你的任务是严格地、只基于上面提供的JSON数据来生成报告。
                不要添加任何数据中没有的信息。如果数据显示为空，请如实说明。
            """),
            expected_output=dedent("""
                一份格式精美的Markdown报告，标题为“近期及未来IPO列表”。
                报告内容严格基于所提供的数据，以项目符号列表的形式展示每个IPO的关键信息。
            """),
            agent=agent
        )