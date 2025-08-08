from __future__ import annotations

import numpy as np
import pandas as pd


def ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    up = np.maximum(delta, 0)
    down = -np.minimum(delta, 0)
    roll_up = pd.Series(up).rolling(period).mean()
    roll_down = pd.Series(down).rolling(period).mean()
    rs = roll_up / (roll_down + 1e-9)
    return 100 - (100 / (1 + rs))


def macd(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> tuple[pd.Series, pd.Series]:
    ema_fast = ema(series, fast)
    ema_slow = ema(series, slow)
    macd_line = ema_fast - ema_slow
    signal_line = ema(macd_line, signal)
    return macd_line, macd_line - signal_line


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    high_low = (df["high"] - df["low"]).abs()
    high_close = (df["high"] - df["close"].shift(1)).abs()
    low_close = (df["low"] - df["close"].shift(1)).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(period).mean()


def vwap(df: pd.DataFrame) -> pd.Series:
    pv = (df["close"] * df["volume"]).cumsum()
    v = df["volume"].cumsum()
    return pv / (v + 1e-9)


def bid_ask_imbalance(bid: pd.Series, ask: pd.Series) -> pd.Series:
    denom = (bid + ask) + 1e-9
    return (bid - ask) / denom


def rolling_zscore(series: pd.Series, window: int = 20) -> pd.Series:
    mean = series.rolling(window).mean()
    std = series.rolling(window).std(ddof=0)
    return (series - mean) / (std + 1e-9)


# Placeholders for options/sentiment features

def implied_vol_rank(iv_series: pd.Series, lookback_days: int = 252) -> pd.Series:
    roll_min = iv_series.rolling(lookback_days).min()
    roll_max = iv_series.rolling(lookback_days).max()
    return (iv_series - roll_min) / (roll_max - roll_min + 1e-9)


def gamma_exposure_placeholder(df_options: pd.DataFrame) -> pd.Series:
    return pd.Series(0.0, index=df_options.index)


def put_call_ratio_placeholder(df_options: pd.DataFrame) -> pd.Series:
    return pd.Series(1.0, index=df_options.index)


def news_sentiment_placeholder(timestamps: pd.Series) -> pd.Series:
    return pd.Series(0.0, index=timestamps)