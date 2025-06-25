# src/tools/custom_tools.py

from typing import Type, Dict, Any, List
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import finnhub
import os

class IPOCalendarInput(BaseModel):
    """Input schema for IPOCalendarTool."""
    from_date: str = Field(..., description="Start date in YYYY-MM-DD format.")
    to_date: str = Field(..., description="End date in YYYY-MM-DD format.")

class IPOCalendarTool(BaseTool):
    name: str = "IPO Calendar Tool"
    description: str = "Fetches upcoming and recent IPOs within a specified date range."
    args_schema: Type[BaseModel] = IPOCalendarInput

    def _run(self, from_date: str, to_date: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        工具的核心执行逻辑。
        现在直接返回一个结构化的字典，而不是字符串。
        """
        api_key = os.environ.get("FINNHUB_API_KEY")
        if not api_key:
            # 对于工具内部错误，返回一个符合预期的空结构，并附带错误信息
            return {"ipos": [{"error": "FINNHUB_API_KEY environment variable not set."}]}

        finnhub_client = finnhub.Client(api_key=api_key)
        
        try:
            response_data = finnhub_client.ipo_calendar(_from=from_date, to=to_date)
            
            if not isinstance(response_data, dict) or 'ipoCalendar' not in response_data:
                return {"ipos": [{"error": f"Finnhub API response is not in the expected format. Response: {str(response_data)}"}]}

            ipo_calendar = response_data['ipoCalendar']
            
            if not isinstance(ipo_calendar, list) or not ipo_calendar:
                return {"ipos": []}  # 如果没有IPO，返回一个空的列表

            # 使用Python代码进行确定性的数据处理和结构化
            structured_ipos = []
            for ipo in ipo_calendar:
                ipo_data = ipo if isinstance(ipo, dict) else ipo.to_dict()
                structured_ipos.append({
                    "company": ipo_data.get('name', 'N/A'),
                    "ticker": ipo_data.get('symbol', 'N/A'),
                    "date": ipo_data.get('date', 'N/A'),
                    "exchange": ipo_data.get('exchange', 'N/A'),
                    "price_range": ipo_data.get('price', 'N/A',), # Finnhub中字段为'price'
                })
            
            # 直接返回符合Pydantic模型结构的字典
            return {"ipos": structured_ipos}

        except Exception as e:
            return {"ipos": [{"error": f"An unexpected error occurred while calling Finnhub API: {e}"}]}

# FinancialTools 工具箱类的定义保持不变
class FinancialTools:
    def __init__(self):
        self.ipo_calendar = IPOCalendarTool()