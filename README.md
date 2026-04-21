# A股量化交易系统

## 项目简介

这是一个用于A股量化交易的个人项目，使用Python开发。

## 项目结构

```
a-quant/
├── src/
│   └── quant/                  # 核心代码
│       ├── __init__.py
│       ├── data.py            # 数据获取模块
│       ├── strategy.py        # 策略模块
│       ├── backtest.py       # 回测模块
│       └── datasources/       # 数据源模块
│           ├── __init__.py
│           ├── tdx_reader.py # 通达信本地数据读取器
│           └── tdx_cache.py  # 数据缓存
├── data/                      # 数据目录
│   ├── raw/                  # 原始数据
│   └── processed/            # 处理后的数据
├── notebooks/                 # Jupyter笔记本
├── logs/                      # 日志文件
├── config/                    # 配置文件
│   ├── config.yaml
│   └── .env.example
├── main.py                    # 主入口
└── pyproject.toml             # 项目配置
```

## 安装依赖

```bash
uv sync
```

## 配置环境

复制环境变量模板文件：

```bash
cp config/.env.example config/.env
```

编辑 `config/.env`，设置通达信数据目录：

```env
TDX_DATA_ROOT=/path/to/your/tdx/vipdoc
```

## 数据获取

### 通达信本地数据

项目已实现通达信本地数据读取功能，支持：

**数据频率**:
- `daily` - 日线数据
- `1min` - 1分钟数据
- `5min` - 5分钟数据

**使用示例**:

```python
from quant.datasources import TdxDataReader

reader = TdxDataReader()

# 读取日线数据
daily_data = reader.get_stock_data("600519", freq="daily")

# 读取5分钟数据
min5_data = reader.get_stock_data("600519", freq="5min")

# 读取1分钟数据
min1_data = reader.get_stock_data("600519", freq="1min")

# 日期范围过滤
data = reader.get_stock_data(
    "600519", 
    start_date="2024-01-01", 
    end_date="2024-12-31", 
    freq="daily"
)

# 支持股票代码格式
# - "600519" - 自动识别为沪市
# - "000001" - 自动识别为深市
# - "sh600519" - 显式指定沪市
# - "sz000001" - 显式指定深市
```

### 数据格式说明

**日线数据 (.day)**:
- 格式: 小端序, 32字节/记录
- 价格单位: 分 (需除以100)
- 字段: 日期, 开盘, 最高, 最低, 收盘, 成交额, 成交量

**分钟数据 (.lc1/.lc5)**:
- 格式: 小端序, 32字节/记录
- 价格: float类型
- 日期编码: year = num/2048 + 2004
- 时间: 从0点开始的分钟数

## 运行项目

```bash
uv run python main.py
```

## 数据源

项目支持以下A股数据接口：
- 通达信本地数据 (已实现)
- Tushare
- AkShare
- BaoStock

## 注意事项

1. 配置通达信数据目录请复制 `config/.env.example` 为 `config/.env` 并填入 `TDX_DATA_ROOT`
2. 数据文件会保存在 `data/` 目录下，已添加到.gitignore中
3. 本地路径、Token、密钥等敏感信息请放在 `.env` 中，不要提交到代码库
