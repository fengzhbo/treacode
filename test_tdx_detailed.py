"""
详细测试通达信数据读取
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from quant.datasources import TdxDataReader

print("=" * 80)
print("1. 读取茅台(600519)日线数据 - 最近5天")
print("=" * 80)

reader = TdxDataReader()
stock_data = reader.get_stock_data("600519", freq="daily")

print(f"\n股票代码: {stock_data.code}")
print(f"市场: {stock_data.market}")
print(f"频率: {stock_data.freq}")
print(f"总记录数: {len(stock_data.data)}")

print("\n最近5天数据:")
print(stock_data.data.tail().to_string())

print("\n" + "=" * 80)
print("2. 读取茅台(600519)5分钟数据 - 最近10条")
print("=" * 80)

min5_data = reader.get_stock_data("600519", freq="5min")

print(f"\n股票代码: {min5_data.code}")
print(f"总记录数: {len(min5_data.data)}")

print("\n最近10条5分钟数据:")
print(min5_data.data.tail(10).to_string())

print("\n" + "=" * 80)
print("3. 读取茅台(600519)1分钟数据 - 最近10条")
print("=" * 80)

min1_data = reader.get_stock_data("600519", freq="1min")

print(f"\n股票代码: {min1_data.code}")
print(f"总记录数: {len(min1_data.data)}")

print("\n最近10条1分钟数据:")
print(min1_data.data.tail(10).to_string())

print("\n" + "=" * 80)
print("4. 读取上证指数(sh000001) - 最近5天")
print("=" * 80)

index_data = reader.get_stock_data("000001", freq="daily")

print(f"\n股票代码: {index_data.code}")
print(f"市场: {index_data.market}")
print(f"总记录数: {len(index_data.data)}")

print("\n最近5天数据:")
print(index_data.data.tail().to_string())

print("\n" + "=" * 80)
print("5. 带日期范围过滤 - 茅台2024年1月")
print("=" * 80)

jan_data = reader.get_stock_data(
    "600519",
    start_date="2024-01-01",
    end_date="2024-01-31",
    freq="daily"
)

print(f"\n日期范围: 2024-01-01 到 2024-01-31")
print(f"记录数: {len(jan_data.data)}")
print("\n数据:")
print(jan_data.data.to_string())

print("\n" + "=" * 80)
print("数据完整性检查")
print("=" * 80)

print(f"\n日线数据列: {list(stock_data.data.columns)}")
print(f"5分钟数据列: {list(min5_data.data.columns)}")
print(f"1分钟数据列: {list(min1_data.data.columns)}")

print(f"\n数据类型:")
print(stock_data.data.dtypes)

print("\n✅ 所有测试完成！")
