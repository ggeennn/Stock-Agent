# src/tools/custom_tools.py

# ... (顶部的import和IPOCalendarInput类保持不变) ...
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import finnhub
import os

class IPOCalendarInput(BaseModel):
    """Input schema for IPOCalendarTool."""
    from_date: str = Field(..., description="Start date in YYYY-MM-DD format.")
    to_date: str = Field(..., description="End date in YYYY-MM-DD format.")


# ⬇️ 请用下面的代码块完整替换你文件中的 IPOCalendarTool 类 ⬇️
class IPOCalendarTool(BaseTool):
    name: str = "IPO Calendar Tool"
    description: str = "Fetches upcoming and recent IPOs within a specified date range."
    args_schema: Type[BaseModel] = IPOCalendarInput

    def _run(self, from_date: str, to_date: str) -> str:
        """工具的核心执行逻辑。"""

        api_key = os.environ.get("FINNHUB_API_KEY")
        if not api_key:
            return "Error: FINNHUB_API_KEY environment variable not set. Please set it in the .env file."

        finnhub_client = finnhub.Client(api_key=api_key)
        
        try:
            response_data = finnhub_client.ipo_calendar(_from=from_date, to=to_date)
            
            # --- 关键修正：检查返回的是否为字典，并从中提取 'ipoCalendar' 列表 ---
            if not isinstance(response_data, dict) or 'ipoCalendar' not in response_data:
                return f"Error: Finnhub API response is not in the expected format. Response: {str(response_data)}"

            ipo_calendar = response_data['ipoCalendar']
            # ------------------------------------------------------------------
            
            if not isinstance(ipo_calendar, list):
                 return f"Error: Expected a list of IPOs inside 'ipoCalendar' key, but got something else. Response: {str(ipo_calendar)}"

            if not ipo_calendar:
                return "No IPOs found in the specified date range."

            formatted_ipos = []
            for ipo in ipo_calendar:
                # 兼容finnhub库可能返回字典或对象的两种情况
                ipo_data = ipo if isinstance(ipo, dict) else ipo.to_dict()
                formatted_ipos.append(
                    f"- Company: {ipo_data.get('name', 'N/A')}, "
                    f"Ticker: {ipo_data.get('symbol', 'N/A')}, "
                    f"Date: {ipo_data.get('date', 'N/A')}, "
                    f"Exchange: {ipo_data.get('exchange', 'N/A')}, "
                    f"Price Range: {ipo_data.get('price', 'N/A')}"
                )
            return "\n".join(formatted_ipos)

        except Exception as e:
            return f"An unexpected error occurred while calling Finnhub API: {e}"