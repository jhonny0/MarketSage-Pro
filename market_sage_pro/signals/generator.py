from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

from ..utils.kelly import kelly_fraction


TradeAction = Literal["BUY", "SHORT", "HOLD", "OPTION_SELL_STRADDLE", "OPTION_BUY_ATM"]


@dataclass
class Signal:
    action: TradeAction
    probability: float
    predicted_move_pct: float
    confidence: int
    size_fraction: float
    stop_loss_pct: float
    target_pct: float
    rationale: str


@dataclass
class SignalConfig:
    kelly_fraction_cap: float


def generate_signal(
    ensemble_up_prob: float,
    ensemble_down_prob: float,
    predicted_move_pct: float,
    rsi: float,
    price_vs_ema21: float,
    ivr: float,
    prob_big_move: float,
    cfg: SignalConfig,
) -> Signal:
    action: TradeAction = "HOLD"
    rationale = []

    # Directional gates
    if predicted_move_pct >= 0.25 and ensemble_up_prob >= 0.70 and rsi < 65 and price_vs_ema21 >= 0:
        action = "BUY"
        rationale.append("Up prob >=0.70, RSI<65, above EMA21")
    elif predicted_move_pct <= -0.25 and ensemble_down_prob >= 0.70 and rsi > 35 and price_vs_ema21 <= 0:
        action = "SHORT"
        rationale.append("Down prob >=0.70, RSI>35, below EMA21")

    # Options play
    if ivr < 0.3 and prob_big_move >= 0.6:
        action = "OPTION_SELL_STRADDLE"
        rationale.append("IVR<0.3 and P(|move|>1%)>=0.6 -> 1SD straddle")
    elif action in ("BUY", "SHORT") and prob_big_move < 0.6:
        action = "OPTION_BUY_ATM"
        rationale.append("Directional + buy 7DTE ATM option")

    # Sizing via Kelly
    win_prob = max(ensemble_up_prob, ensemble_down_prob)
    win_loss_ratio = max(1.0, abs(predicted_move_pct) / 0.5)
    kelly = kelly_fraction(win_prob, win_loss_ratio)
    size_frac = min(kelly * win_prob, cfg.kelly_fraction_cap)

    # Stops/targets simple
    stop = -abs(predicted_move_pct) * 0.8
    target = abs(predicted_move_pct) * 1.5

    confidence = int(round(win_prob * 100))

    return Signal(
        action=action,
        probability=win_prob,
        predicted_move_pct=predicted_move_pct,
        confidence=confidence,
        size_fraction=size_frac,
        stop_loss_pct=stop,
        target_pct=target,
        rationale="; ".join(rationale) or "No edge",
    )