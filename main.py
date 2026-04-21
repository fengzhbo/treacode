"""
A股量化交易项目主入口
"""
from loguru import logger
import yaml
from pathlib import Path


def load_config():
    """加载配置文件"""
    config_path = Path("config/config.yaml")
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}


def main():
    logger.info("欢迎使用A股量化交易系统")
    
    config = load_config()
    logger.info(f"配置加载完成: {config}")
    
    # TODO: 添加你的策略逻辑
    logger.info("项目已初始化，请开始你的量化之旅！")


if __name__ == "__main__":
    main()
