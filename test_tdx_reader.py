"""
测试通达信数据读取功能
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from quant.datasources import TdxDataReader, StockData

def test_read_stock_data():
    print("=" * 60)
    print("测试读取股票数据")
    print("=" * 60)

    reader = TdxDataReader()

    try:
        print("\n1. 读取上证指数 (sh000001) 日线数据...")
        stock_data = reader.get_stock_data("000001", freq="daily")
        print(f"   代码: {stock_data.code}")
        print(f"   市场: {stock_data.market}")
        print(f"   频率: {stock_data.freq}")
        print(f"   数据行数: {len(stock_data.data)}")
        if not stock_data.data.empty:
            print(f"   日期范围: {stock_data.data['date'].min()} 到 {stock_data.data['date'].max()}")
            print(f"\n   前5条数据:")
            print(stock_data.data.head())
    except Exception as e:
        print(f"   ✗ 读取失败: {e}")

    try:
        print("\n2. 读取深证成指 (sz399001) 日线数据...")
        stock_data = reader.get_stock_data("399001", freq="daily")
        print(f"   代码: {stock_data.code}")
        print(f"   市场: {stock_data.market}")
        print(f"   数据行数: {len(stock_data.data)}")
        if not stock_data.data.empty:
            print(f"   日期范围: {stock_data.data['date'].min()} 到 {stock_data.data['date'].max()}")
            print(f"\n   前5条数据:")
            print(stock_data.data.head())
    except Exception as e:
        print(f"   ✗ 读取失败: {e}")

    try:
        print("\n3. 读取带日期范围的茅台日线数据...")
        stock_data = reader.get_stock_data(
            "600519",
            start_date="2024-01-01",
            end_date="2024-12-31",
            freq="daily"
        )
        print(f"   代码: {stock_data.code}")
        print(f"   数据行数: {len(stock_data.data)}")
        if not stock_data.data.empty:
            print(f"   日期范围: {stock_data.data['date'].min()} 到 {stock_data.data['date'].max()}")
            print(f"\n   前5条数据:")
            print(stock_data.data.head())
    except Exception as e:
        print(f"   ✗ 读取失败: {e}")

    try:
        print("\n4. 列出可用的上海市场日线股票...")
        stocks = reader.list_available_stocks(market="sh", freq="daily")
        print(f"   上海市场日线股票数量: {len(stocks)}")
        print(f"   前10个: {stocks[:10]}")
    except Exception as e:
        print(f"   ✗ 列出失败: {e}")

    try:
        print("\n5. 测试读取5分钟数据...")
        stock_data = reader.get_stock_data("600519", freq="5min")
        print(f"   代码: {stock_data.code}")
        print(f"   数据行数: {len(stock_data.data)}")
        if not stock_data.data.empty:
            print(f"   时间范围: {stock_data.data['date'].min()} 到 {stock_data.data['date'].max()}")
            print(f"\n   前5条数据:")
            print(stock_data.data.head())
    except Exception as e:
        print(f"   ✗ 读取失败: {e}")

    try:
        print("\n6. 测试读取1分钟数据...")
        stock_data = reader.get_stock_data("600519", freq="1min")
        print(f"   代码: {stock_data.code}")
        print(f"   数据行数: {len(stock_data.data)}")
        if not stock_data.data.empty:
            print(f"   时间范围: {stock_data.data['date'].min()} 到 {stock_data.data['date'].max()}")
            print(f"\n   前5条数据:")
            print(stock_data.data.head())
    except Exception as e:
        print(f"   ✗ 读取失败: {e}")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_read_stock_data()
