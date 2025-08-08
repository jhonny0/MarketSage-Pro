from __future__ import annotations

import numpy as np


def soft_vote(hourly_proba: np.ndarray, daily_proba: np.ndarray, mode: str = "intraday") -> np.ndarray:
    if mode == "intraday":
        w_hourly, w_daily = 0.6, 0.4
    else:
        w_hourly, w_daily = 0.4, 0.6
    return np.clip(w_hourly * hourly_proba + w_daily * daily_proba, 0.0, 1.0)