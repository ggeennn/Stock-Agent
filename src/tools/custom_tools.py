# src/tools/custom_tools.py

from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import finnhub
import os

# Data Model现在也在这里定义，符合你的模块化思想
class IPOCalendarInput(BaseModel):
    """Input schema for IPOCalendarTool."""
    from_date: str = Field(..., description="Start date in YYYY-MM-DD format.")
    to_date: str = Field(..., description="End date in YYYY-MM-DD format.")

class IPOCalendarTool(BaseTool):
    name: str = "IPO Calendar Tool"
    description: str = "Fetches upcoming and recent IPOs within a specified date range."
    args_schema: Type[BaseModel] = IPOCalendarInput

    def _run(self, from_date: str, to_date: str) -> dict: # <-- 返回值类型是dict
        api_key = os.environ.get("FINNHUB_API_KEY")
        if not api_key:
            return {"error": "FINNHUB_API_KEY environment variable not set."}

        finnhub_client = finnhub.Client(api_key=api_key)
        try:
            response_data = finnhub_client.ipo_calendar(_from=from_date, to=to_date)
            
            if not isinstance(response_data, dict) or 'ipoCalendar' not in response_data:
                return {"error": f"Finnhub API response not in expected format. Response: {str(response_data)}"}

            ipo_calendar = response_data['ipoCalendar']
            
            if not ipo_calendar:
                return {"ipos": []}

            structured_ipos = [
                {
                    "company_name": ipo.get('name', 'N/A'),
                    "ticker": ipo.get('symbol', 'N/A'),
                    "ipo_date": ipo.get('date', 'N/A'),
                    "exchange": ipo.get('exchange', 'N/A'),
                    "price_range": ipo.get('price', 'N/A')
                } for ipo in ipo_calendar
            ]
            return {"ipos": structured_ipos}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {e}"}