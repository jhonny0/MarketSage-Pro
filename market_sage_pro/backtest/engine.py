from __future__ import annotations

import argparse
from datetime import datetime
from typing import List

import numpy as np
import pandas as pd

from ..signals.generator import Signal, SignalConfig, generate_signal


def backtest(df: pd.DataFrame, cfg: SignalConfig) -> dict:
    equity = 1.0
    peak = 1.0
    returns: List[float] = []
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--from", dest="from_date", required=True)
    parser.add_argument("--to", dest="to_date", required=True)
    parser.add_argument("--symbols", type=str, required=True)
    args = parser.parse_args()

    # Placeholder data
    dates = pd.date_range(start="2023-01-01", end=datetime.utcnow(), freq="B")
    df = pd.DataFrame(
        {
            "p_up": 0.55,
            "p_down": 0.45,
            "pred_move": 0.3,
            "rsi": 50,
            "px_vs_ema21": 1,
            "ivr": 0.2,
            "p_big": 0.7,
            "actual_move": np.random.normal(0.05, 0.5, size=len(dates)),
        },
        index=dates,
    )

    res = backtest(df, SignalConfig(kelly_fraction_cap=0.5))
    for k, v in res.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()