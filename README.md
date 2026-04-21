# A股量化交易系统

## 项目简介

这是一个用于A股量化交易的个人项目，使用Python开发。

## 项目结构

```
a-quant/
├── src/
│   └── quant/          # 核心代码
│       ├── __init__.py
│       ├── data.py      # 数据获取模块
│       ├── strategy.py  # 策略模块
│       └── backtest.py # 回测模块
├── data/              # 数据目录
│   ├── raw/          # 原始数据
│   └── processed/    # 处理后的数据
├── notebooks/         # Jupyter笔记本
├── logs/            # 日志文件
├── config/          # 配置文件
│   ├── config.yaml
│   └── .env.example
├── main.py          # 主入口
└── pyproject.toml   # 项目配置
```

## 安装依赖

```bash
uv sync
```

## 运行项目

```bash
uv run python main.py
```

## 数据源

项目支持以下A股数据接口：
- Tushare
- AkShare
- BaoStock

## 注意事项

1. 配置API密钥请复制 `config/.env.example` 为 `config/.env` 并填入你的密钥
2. 数据文件会保存在 `data/` 目录下，已添加到.gitignore中
