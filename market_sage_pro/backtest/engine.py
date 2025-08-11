from __future__ import annotations

import argparse
from datetime import datetime

import numpy as np
import pandas as pd

from ..data.features import ema, rsi
from ..data.store import fetch_historical_bars
from ..signals.generator import Signal, SignalConfig, generate_signal


def backtest(df: pd.DataFrame, cfg: SignalConfig) -> dict[str, float | int]:
    equity = 1.0
    peak = 1.0
    returns: list[float] = []
    wins = 0
    trades = 0
    for _, row in df.iterrows():
        sig: Signal = generate_signal(
            ensemble_up_prob=row.get("p_up", 0.5),
            ensemble_down_prob=row.get("p_down", 0.5),
            predicted_move_pct=row.get("pred_move", 0.0),
            rsi=row.get("rsi", 50.0),
            price_vs_ema21=row.get("px_vs_ema21", 0.0),
            ivr=row.get("ivr", 0.5),
            prob_big_move=row.get("p_big", 0.5),
            cfg=cfg,
        )
        if sig.action == "HOLD":
            returns.append(0.0)
            continue
        ret = row.get("actual_move", 0.0) / 100.0
        trades += 1
        if ret > 0:
            wins += 1
        equity *= (1 + ret * sig.size_fraction)
        peak = max(peak, equity)
        returns.append(ret * sig.size_fraction)

    arr = np.array(returns)
    cagr = (equity) ** (252 / max(1, len(arr))) - 1
    dd = (peak - equity) / peak if peak > 0 else 0.0
    sharpe = (arr.mean() / (arr.std(ddof=1) + 1e-9)) * np.sqrt(252)
    sortino = (arr.mean() / (arr[arr < 0].std(ddof=1) + 1e-9)) * np.sqrt(252)
    win_rate = wins / max(1, trades)
    profit_factor = arr[arr > 0].sum() / (abs(arr[arr < 0].sum()) + 1e-9)

    return {
        "CAGR": cagr,
        "max_drawdown": dd,
        "Sharpe": sharpe,
        "Sortino": sortino,
        "win_rate": win_rate,
        "profit_factor": profit_factor,
        "trades": trades,
        "equity": equity,
    }


def _prepare_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["rsi"] = rsi(df["close"]).fillna(50)
    df["ema21"] = ema(df["close"], span=21)
    df["px_vs_ema21"] = ((df["close"] - df["ema21"]) / df["ema21"]).fillna(0)
    df["actual_move"] = df["close"].pct_change() * 100
    df["pred_move"] = df["actual_move"].shift(1).fillna(0)
    df["p_up"] = np.where(df["pred_move"] >= 0, 0.7, 0.3)
    df["p_down"] = 1 - df["p_up"]
    df["ivr"] = 0.5
    df["p_big"] = 0.7
    return df.dropna(subset=["actual_move"])


def run_backtest(symbols: list[str], start: datetime, end: datetime) -> dict[str, dict[str, float | int]]:
    results = {}
    for sym in symbols:
        bars = fetch_historical_bars(sym, start, end)
        if bars.empty:
            continue
        df = _prepare_df(bars)
        results[sym] = backtest(df, SignalConfig(kelly_fraction_cap=0.5))
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--from", dest="from_date", required=True)
    parser.add_argument("--to", dest="to_date", required=True)
    parser.add_argument("--symbols", type=str, required=True)
    args = parser.parse_args()

    start = datetime.fromisoformat(args.from_date)
    end = datetime.utcnow() if args.to_date.lower() == "today" else datetime.fromisoformat(args.to_date)
    symbols = [s.strip() for s in args.symbols.split(",")]

    res = run_backtest(symbols, start, end)
    for sym, metrics in res.items():
        print(sym)
        for k, v in metrics.items():
            print(f"{k}: {v}")


if __name__ == "__main__":
    main()