"""
通达信本地数据读取器
"""
import os
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime, timedelta
import math

import pandas as pd
from dotenv import load_dotenv

load_dotenv()


@dataclass
class StockData:
    code: str
    name: str
    market: str
    freq: str
    data: pd.DataFrame


class TdxDataReader:
    RECORD_SIZE = 32

    FREQ_CONFIG = {
        "daily": ("lday", ".day"),
        "1min": ("minline", ".lc1"),
        "5min": ("fzline", ".lc5"),
    }

    MARKET_MAP = {
        "sh": "sh",
        "sz": "sz",
        "bj": "bj",
    }

    def __init__(self, data_root: Optional[str] = None):
        if data_root is None:
            data_root = os.getenv("TDX_DATA_ROOT")
            if data_root is None:
                raise ValueError(
                    "TDX_DATA_ROOT environment variable is not set. "
                    "Please configure it in your .env file."
                )

        self.data_root = Path(data_root)
        if not self.data_root.exists():
            raise FileNotFoundError(f"Data root directory not found: {self.data_root}")

    def _parse_stock_code(self, code: str) -> tuple[str, str]:
        if code.startswith(("sh", "sz", "bj")):
            if len(code) != 8:
                raise ValueError(f"Invalid stock code format: {code}")
            market = code[:2]
            stock_code = code[2:]
        else:
            if len(code) != 6:
                raise ValueError(f"Invalid stock code format: {code}")
            if code.startswith(("000", "001", "002", "003", "399")):
                market = "sz"
            elif code.startswith(("600", "601", "603", "605", "688")):
                market = "sh"
            elif code.startswith(("8", "4", "830", "831")):
                market = "bj"
            else:
                raise ValueError(f"Cannot determine market for code: {code}")
            stock_code = code

        return market, stock_code

    def _get_file_path(self, code: str, freq: str) -> Path:
        market, stock_code = self._parse_stock_code(code)
        freq_config = self.FREQ_CONFIG.get(freq)
        if freq_config is None:
            raise ValueError(f"Unsupported frequency: {freq}")

        freq_dir, _ = freq_config

        if self.data_root.name == "vipdoc":
            vipdoc_path = self.data_root
        else:
            vipdoc_path = self.data_root / "vipdoc"

        file_path = vipdoc_path / market / freq_dir / f"{market}{stock_code}"

        return file_path

    def _read_daily_file(self, file_path: Path) -> List[Dict]:
        if not file_path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")

        records = []
        with open(file_path, "rb") as f:
            while True:
                data = f.read(self.RECORD_SIZE)
                if not data:
                    break
                if len(data) != self.RECORD_SIZE:
                    break

                date_int, open_int, high_int, low_int, close_int, amount, volume, _ = struct.unpack("<IIIIIfII", data)

                if date_int == 0:
                    continue

                year = date_int // 10000
                month = (date_int % 10000) // 100
                day = date_int % 100

                if year < 1990 or year > 2100:
                    continue

                records.append({
                    "date": datetime(year, month, day),
                    "open": open_int / 100.0,
                    "high": high_int / 100.0,
                    "low": low_int / 100.0,
                    "close": close_int / 100.0,
                    "volume": volume,
                    "amount": amount,
                })

        return records

    def _read_minute_file(self, file_path: Path) -> List[Dict]:
        if not file_path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")

        records = []
        with open(file_path, "rb") as f:
            while True:
                data = f.read(self.RECORD_SIZE)
                if not data:
                    break
                if len(data) != self.RECORD_SIZE:
                    break

                date_val = struct.unpack("<H", data[0:2])[0]
                minute_offset = struct.unpack("<H", data[2:4])[0]

                open_price = struct.unpack("<f", data[4:8])[0]
                high_price = struct.unpack("<f", data[8:12])[0]
                low_price = struct.unpack("<f", data[12:16])[0]
                close_price = struct.unpack("<f", data[16:20])[0]
                amount = struct.unpack("<f", data[20:24])[0]
                volume = struct.unpack("<I", data[24:28])[0]

                if date_val == 0:
                    continue

                year = math.floor(date_val / 2048) + 2004
                month = math.floor((date_val % 2048) / 100)
                day = (date_val % 2048) % 100

                if year < 1990 or year > 2100 or month < 1 or month > 12 or day < 1 or day > 31:
                    continue

                hour = minute_offset // 60
                minute = minute_offset % 60

                records.append({
                    "date": datetime(year, month, day, hour, minute),
                    "open": open_price,
                    "high": high_price,
                    "low": low_price,
                    "close": close_price,
                    "volume": volume,
                    "amount": amount,
                })

        return records

    def _read_binary_file(self, file_path: Path, freq: str) -> List[Dict]:
        if freq == "daily":
            return self._read_daily_file(file_path)
        else:
            return self._read_minute_file(file_path)

    def _filter_by_date(
        self,
        records: List[Dict],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Dict]:
        if start_date is None and end_date is None:
            return records

        filtered = []
        start_dt = pd.to_datetime(start_date) if start_date else None
        end_dt = pd.to_datetime(end_date) if end_date else None

        for record in records:
            if start_dt and record["date"] < start_dt:
                continue
            if end_dt and record["date"] > end_dt:
                continue
            filtered.append(record)

        return filtered

    def get_stock_data(
        self,
        code: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        freq: str = "daily",
    ) -> StockData:
        file_path = self._get_file_path(code, freq)
        freq_config = self.FREQ_CONFIG.get(freq)
        _, file_ext = freq_config
        file_path = file_path.with_suffix(file_ext)

        market, stock_code = self._parse_stock_code(code)

        records = self._read_binary_file(file_path, freq)
        records = self._filter_by_date(records, start_date, end_date)

        df = pd.DataFrame(records)
        if not df.empty:
            df = df.sort_values("date").reset_index(drop=True)

        return StockData(
            code=stock_code,
            name="",
            market=market,
            freq=freq,
            data=df,
        )

    def get_index_data(
        self,
        code: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> StockData:
        return self.get_stock_data(code, start_date, end_date, freq="daily")

    def list_available_stocks(
        self,
        market: str = "all",
        freq: str = "daily",
    ) -> List[str]:
        freq_config = self.FREQ_CONFIG.get(freq)
        if freq_config is None:
            raise ValueError(f"Unsupported frequency: {freq}")

        freq_dir, file_ext = freq_config

        if self.data_root.name == "vipdoc":
            vipdoc_path = self.data_root
        else:
            vipdoc_path = self.data_root / "vipdoc"

        markets = [market] if market != "all" else ["sh", "sz", "bj"]

        stock_codes = []
        for mkt in markets:
            market_path = vipdoc_path / mkt / freq_dir
            if not market_path.exists():
                continue

            for file_path in market_path.glob(f"*{file_ext}"):
                code = file_path.stem
                stock_codes.append(code)

        return sorted(stock_codes)
