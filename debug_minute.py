"""
调试 - 推断分钟数据的日期范围
"""
import sys
from pathlib import Path
import os
from datetime import datetime, timedelta

lc1_file = Path("/mnt/d/new_tdx64/vipdoc/sh/minline/sh600519.lc1")

print("=" * 60)
print("推断分钟数据日期范围")
print("=" * 60)

file_size = os.path.getsize(lc1_file)
record_count = file_size // 32
print(f"文件: {lc1_file}")
print(f"文件大小: {file_size}")
print(f"记录数: {record_count}")

mtime = datetime.fromtimestamp(lc1_file.stat().st_mtime)
print(f"文件修改时间: {mtime}")

print(f"\n每天1分钟数据大约: 240条 (4小时 * 60分钟)")
days_of_data = record_count // 240
print(f"推断数据覆盖天数: {days_of_data} 天")

start_date = mtime - timedelta(days=days_of_data)
print(f"推断起始日期: {start_date}")

print("\n" + "=" * 60)
print("分钟数据格式总结")
print("=" * 60)
print("""
通达信分钟数据(.lc1/.lc5)格式 (每记录32字节):
  字段0 (4字节): 小端序int - 未知用途（可能包含日期时间信息但编码特殊）
  字段1 (4字节): 小端序float - 开盘价
  字段2 (4字节): 小端序float - 最高价
  字段3 (4字节): 小端序float - 最低价
  字段4 (4字节): 小端序float - 收盘价
  字段5 (4字节): 小端序int - 成交额
  字段6 (4字节): 小端序int - 成交量
  字段7 (4字节): 小端序int - 保留字段

注意: 日期信息无法直接从数据中解析，需要从文件名或外部数据源获取
""")
