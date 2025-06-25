# src/data_models.py
from pydantic import BaseModel, Field
from typing import List

class IPOInfo(BaseModel):
    """定义单个IPO信息的结构。"""
    company_name: str = Field(..., description="公司的完整名称。")
    ticker: str = Field(..., description="公司的股票代码。")
    ipo_date: str = Field(..., description="预估的IPO日期，格式为 YYYY-MM-DD。")
    # 我们可以根据需要添加更多字段，比如交易所、价格范围等

class IPOReport(BaseModel):
    """定义最终IPO报告的结构，它包含一个IPO信息列表。"""
    ipos: List[IPOInfo] = Field(..., description="一个包含所有已发现的IPO信息的列表。")