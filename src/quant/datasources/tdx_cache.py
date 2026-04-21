"""
数据缓存模块
"""
import os
from pathlib import Path
from typing import Optional, Dict
from functools import lru_cache

import pandas as pd
from dotenv import load_dotenv

load_dotenv()


class DataCache:
    def __init__(self, cache_dir: Optional[str] = None):
        if cache_dir is None:
            cache_dir = os.getenv("TDX_CACHE_DIR", "data/cache")

        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, code: str, freq: str, start_date: Optional[str], end_date: Optional[str]) -> str:
        start = start_date or "start"
        end = end_date or "end"
        return f"{code}_{freq}_{start}_{end}.parquet"

    def get(self, code: str, freq: str, start_date: Optional[str], end_date: Optional[str]) -> Optional[pd.DataFrame]:
        cache_key = self._get_cache_key(code, freq, start_date, end_date)
        cache_path = self.cache_dir / cache_key

        if cache_path.exists():
            try:
                return pd.read_parquet(cache_path)
            except Exception:
                return None

        return None

    def set(self, code: str, freq: str, start_date: Optional[str], end_date: Optional[str], df: pd.DataFrame) -> None:
        cache_key = self._get_cache_key(code, freq, start_date, end_date)
        cache_path = self.cache_dir / cache_key

        df.to_parquet(cache_path, index=False)

    def clear(self) -> None:
        for cache_file in self.cache_dir.glob("*.parquet"):
            cache_file.unlink()

    def get_cache_size(self) -> int:
        return len(list(self.cache_dir.glob("*.parquet")))
