from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable

import duckdb
import pandas as pd

from ..utils.logging import get_logger

logger = get_logger(__name__)


class DuckDBStore:
    def __init__(self, db_path: str = "data/market.duckdb") -> None:
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(db_path)

    def write_bars(self, symbol: str, df: pd.DataFrame) -> None:
        if df.empty:
            return
        df = df.copy()
        df["ts"] = pd.to_datetime(df["ts"], utc=True)
        table = self._table_name(symbol)
        self.conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table} (
                ts TIMESTAMP,
                open DOUBLE,
                high DOUBLE,
                low DOUBLE,
                close DOUBLE,
                volume DOUBLE
            )
            """
        )
        self.conn.register("tmp_df", df)
        self.conn.execute(f"INSERT INTO {table} SELECT * FROM tmp_df")
        self.conn.unregister("tmp_df")
        self.vacuum_retention(table)

    def read_bars(self, symbol: str, since_days: int = 180) -> pd.DataFrame:
        table = self._table_name(symbol)
        try:
            cutoff = datetime.utcnow() - timedelta(days=since_days)
            q = f"SELECT * FROM {table} WHERE ts >= ? ORDER BY ts"
            return self.conn.execute(q, [cutoff]).fetchdf()
        except duckdb.CatalogException:
            return pd.DataFrame(columns=["ts", "open", "high", "low", "close", "volume"])  # empty

    def vacuum_retention(self, table: str, days: int = 180) -> None:
        cutoff = datetime.utcnow() - timedelta(days=days)
        self.conn.execute(f"DELETE FROM {table} WHERE ts < ?", [cutoff])
        # DuckDB VACUUM is global
        self.conn.execute("VACUUM")

    @staticmethod
    def _table_name(symbol: str) -> str:
        return f"bars_{symbol.upper()}"