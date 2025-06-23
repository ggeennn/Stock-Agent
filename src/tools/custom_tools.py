from crewai_tools import BaseTool
from pydantic import BaseModel, Field
import finnhub # 我们需要先安装这个库
import os

# 1. 定义工具的输入模型 (Pydantic Schema)
class IPOCalendarInput(BaseModel):
    """Input schema for IPOCalendarTool."""
    from_date: str = Field(..., description="Start date in YYYY-MM-DD format.")
    to_date: str = Field(..., description="End date in YYYY-MM-DD format.")

# 2. 定义自定义工具类
class IPOCalendarTool(BaseTool):
    name: str = "IPO Calendar Tool"
    description: str = "Fetches upcoming and recent IPOs within a specified date range."
    args_schema = IPOCalendarInput

    def _run(self, from_date: str, to_date: str) -> str:
        # 实例化 Finnhub 客户端
        # 注意：我们将从环境变量中安全地获取API密钥
        finnhub_client = finnhub.Client(api_key=os.environ.get("FINNHUB_API_KEY"))

        try:
            # 调用API
            ipo_calendar = finnhub_client.ipo_calendar(_from=from_date, to=to_date)

            if not ipo_calendar:
                return "No IPOs found in the specified date range."

            # 将JSON结果格式化为易于阅读的字符串
            formatted_ipos = []
            for ipo in ipo_calendar:
                formatted_ipos.append(
                    f"- Company: {ipo.get('name', 'N/A')}, "
                    f"Ticker: {ipo.get('symbol', 'N/A')}, "
                    f"Date: {ipo.get('date', 'N/A')}, "
                    f"Exchange: {ipo.get('exchange', 'N/A')}, "
                    f"Price Range: {ipo.get('price', 'N/A')}"
                )
            return "\n".join(formatted_ipos)

        except Exception as e:
            return f"An error occurred while fetching IPO data: {e}"