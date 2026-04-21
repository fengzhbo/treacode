"""
供人工检查的股票数据输出
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from quant.datasources import TdxDataReader

reader = TdxDataReader()

print("=" * 80)
print("1. 上证指数 (sh000001) 日线数据 - 最近5天")
print("=" * 80)

index_data = reader.get_stock_data("000001", freq="daily")
print(f"\n代码: {index_data.code}, 市场: {index_data.market}")
print("\n最近5天数据:")
print(index_data.data.tail().to_string())

print("\n" + "=" * 80)
print("2. 贵州茅台 (600519) - 日线、1分钟、5分钟数据")
print("=" * 80)

stock1 = reader.get_stock_data("600519", freq="daily")
print(f"\n代码: {stock1.code}, 市场: {stock1.market}")
print("\n最近5天日线数据:")
print(stock1.data.tail().to_string())

stock1_min5 = reader.get_stock_data("600519", freq="5min")
print(f"\n最近10条5分钟数据 (共{len(stock1_min5.data)}条):")
print(stock1_min5.data.tail(10).to_string())

stock1_min1 = reader.get_stock_data("600519", freq="1min")
print(f"\n最近10条1分钟数据 (共{len(stock1_min1.data)}条):")
print(stock1_min1.data.tail(10).to_string())

print("\n" + "=" * 80)
print("3. 平安银行 (000001) - 日线、1分钟、5分钟数据")
print("=" * 80)

stock2 = reader.get_stock_data("000001", freq="daily")
print(f"\n代码: {stock2.code}, 市场: {stock2.market}")
print("\n最近5天日线数据:")
print(stock2.data.tail().to_string())

stock2_min5 = reader.get_stock_data("000001", freq="5min")
print(f"\n最近10条5分钟数据 (共{len(stock2_min5.data)}条):")
print(stock2_min5.data.tail(10).to_string())

stock2_min1 = reader.get_stock_data("000001", freq="1min")
print(f"\n最近10条1分钟数据 (共{len(stock2_min1.data)}条):")
print(stock2_min1.data.tail(10).to_string())

print("\n" + "=" * 80)
print("4. 浦发银行 (600000) - 日线、1分钟、5分钟数据")
print("=" * 80)

stock3 = reader.get_stock_data("600000", freq="daily")
print(f"\n代码: {stock3.code}, 市场: {stock3.market}")
print("\n最近5天日线数据:")
print(stock3.data.tail().to_string())

stock3_min5 = reader.get_stock_data("600000", freq="5min")
print(f"\n最近10条5分钟数据 (共{len(stock3_min5.data)}条):")
print(stock3_min5.data.tail(10).to_string())

stock3_min1 = reader.get_stock_data("600000", freq="1min")
print(f"\n最近10条1分钟数据 (共{len(stock3_min1.data)}条):")
print(stock3_min1.data.tail(10).to_string())

print("\n" + "=" * 80)
print("5. 5分钟数据验证 - 检查是否是5分钟的间隔")
print("=" * 80)

print("\n茅台(600519) 5分钟数据前20条:")
for i, row in stock1_min5.data.head(20).iterrows():
    print(f"{row['date'].strftime('%Y-%m-%d %H:%M')} | O:{row['open']:.2f} H:{row['high']:.2f} L:{row['low']:.2f} C:{row['close']:.2f} V:{row['volume']}")

print("\n" + "=" * 80)
print("6. 1分钟数据验证 - 检查是否是1分钟的间隔")
print("=" * 80)

print("\n平安银行(000001) 1分钟数据前20条:")
for i, row in stock2_min1.data.head(20).iterrows():
    print(f"{row['date'].strftime('%Y-%m-%d %H:%M')} | O:{row['open']:.2f} H:{row['high']:.2f} L:{row['low']:.2f} C:{row['close']:.2f} V:{row['volume']}")

print("\n✅ 数据输出完成，请人工检查！")
