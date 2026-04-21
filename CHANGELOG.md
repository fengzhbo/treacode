# CHANGELOG

## 2026-04-22 - 数据获取层实现

### 新增
- **通达信本地数据读取器 (TdxDataReader)
  - 支持日线数据 (daily)
  - 支持1分钟数据 (1min)
  - 支持5分钟数据 (5min)
  - 支持自动识别沪市(sh)、深市(sz)、北交所(bj)
- **数据缓存模块** (tdx_cache.py)
- **datasources 模块结构

### 修复
- 修正日线数据volume和amount字段顺序错误
- 修正日线数据字段类型：amount为float，volume为int

### 数据格式
- 日线数据：struct格式：`<IIIIIfII`
- 分钟数据：日期编码 year = num/2048 + 2004
- 分钟数据：时间从0点开始的分钟数

### 配置
- 敏感配置通过环境变量 `TDX_DATA_ROOT` 读取
- 配置文件：config/.env
