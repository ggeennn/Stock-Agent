# src/tasks.py

from crewai import Task
from textwrap import dedent
from datetime import datetime, timedelta
# ⬇️ 新增导入 ⬇️
from pydantic import BaseModel, Field
from typing import List

# ⬇️ 1. 定义期望的输出结构 (Pydantic模型) ⬇️
class SingleIPO(BaseModel):
    """一个IPO项目的数据模型"""
    company: str = Field(..., description="公司名称")
    ticker: str = Field(..., description="股票代码")
    date: str = Field(..., description="上市日期")
    exchange: str = Field(..., description="交易所")
    price_range: str = Field(..., description="价格区间")

class IPOList(BaseModel):
    """包含多个IPO项目列表的数据模型"""
    ipos: List[SingleIPO]

class StockAnalysisTasks():
    
    # ⬇️ 2. 修改数据采集任务，强制使用JSON输出 ⬇️
    def ipo_data_gathering_task(self, agent):
        """
        任务一：纯粹的数据采集任务。
        它的唯一目标就是调用工具并以严格的JSON格式返回数据。
        """
        today = datetime.now()
        end_date = (today + timedelta(days=90)).strftime("%Y-%m-%d")
        start_date = today.strftime("%Y-%m-%d")

        return Task(
            description=dedent(f"""
                调用你的IPO日历工具，获取从 {start_date} 到 {end_date} 的所有IPO数据。
                你的任务是分析工具返回的文本，并将其严格地、无遗漏地解析成指定的JSON格式。
                绝对不允许添加任何工具输出中不存在的信息。
            """),
            expected_output=dedent("""
                一个JSON对象，该对象严格遵守你被提供的Pydantic模型（IPOList）的结构。
                它必须包含一个名为 'ipos' 的键，其值为一个列表，列表中的每个对象都代表一个IPO。
            """),
            agent=agent,
            # 关键：告诉Agent必须输出一个符合IPOList模型的JSON
            output_json=IPOList
        )

    # ⬇️ 3. 修改报告生成任务，以处理JSON输入 ⬇️
    def ipo_report_generation_task(self, agent, context):
        """
        任务二：纯粹的报告生成任务。
        它接收任务一的JSON输出作为上下文，并只基于该上下文生成报告。
        """
        return Task(
            description=dedent("""
                仔细审查提供给你的上下文（Context），其中包含了一个关于IPO数据的JSON对象。
                你的唯一任务是遍历这个JSON对象中的每一个IPO项目，并根据其中的信息生成一份格式化的Markdown报告。
                
                **极其重要的规则**:
                1. 绝对不允许使用任何工具。
                2. 绝对不允许从你自己的知识库中添加任何JSON对象中没有明确提及的IPO信息。
                3. 如果JSON对象中的'ipos'列表为空，你的报告就必须如实地反映这一点。
            """),
            expected_output=dedent("""
                一份格式精美的Markdown报告，标题为“近期及未来IPO列表”。
                报告内容严格基于所提供的JSON上下文，以项目符号列表的形式展示每个IPO的关键信息。
            """),
            agent=agent,
            context=context
        )