from crewai import Task
from textwrap import dedent

class StockAnalysisTasks():
    def ipo_discovery_task(self, agent):
        """
        这个任务负责让IPO Scout智能体执行IPO机会的发现工作。
        注意：它接收一个'agent'作为输入，这个agent就是被分配执行此任务的智能体。
        """
        return Task(
            description=dedent(f"""
                扫描从今天到未来90天内所有即将进行和近期已定价的首次公开募股（IPO）。
                对每一个发现的IPO，提供其公司名称、股票代码、预估的上市日期和交易所。
                同时，扫描主流科技和金融新闻源，查找可能预示未来IPO的重大近期融资轮次（例如A轮、B轮或C轮融资）。
                将所有发现结构化地整理成一份简洁的报告。
            """),
            expected_output=dedent("""
                一份Markdown格式的报告，包含两个部分：

                第一部分是“近期及未来IPO列表”，以列表形式展示每个IPO的关键信息（公司名称、股票代码、日期、交易所）。

                第二部分是“重大风险投资观察”，列出近期值得关注的大额融资事件及其相关公司。
            """),
            # 将任务分配给传入的agent
            agent=agent
        )

    # 我们将在这里继续为其他智能体添加任务...