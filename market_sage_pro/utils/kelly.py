from __future__ import annotations


def kelly_fraction(win_prob: float, win_loss_ratio: float) -> float:
    p = max(0.0, min(1.0, win_prob))
    b = max(1e-9, win_loss_ratio)
    f = (p * (b + 1) - 1) / b
    return max(0.0, f)