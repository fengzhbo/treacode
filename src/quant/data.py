"""
数据获取模块 - 统一接口
"""
from typing import Optional
from .datasources import TdxDataReader, StockData


def get_stock_data(
    code: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    freq: str = "daily",
    use_cache: bool = True,
) -> StockData:
    reader = TdxDataReader()
    return reader.get_stock_data(code, start_date, end_date, freq)


def get_index_data(
    code: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> StockData:
    reader = TdxDataReader()
    return reader.get_index_data(code, start_date, end_date)


def list_available_stocks(
    market: str = "all",
    freq: str = "daily",
) -> list[str]:
    reader = TdxDataReader()
    return reader.list_available_stocks(market, freq)
