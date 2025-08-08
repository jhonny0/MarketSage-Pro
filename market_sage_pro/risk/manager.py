from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RiskConfig:
    max_daily_loss_pct: float  # negative number, e.g., -2
    per_symbol_cap_pct: float = 5.0


class RiskManager:
    def __init__(self, cfg: RiskConfig) -> None:
        self.cfg = cfg
        self.daily_pnl_pct = 0.0
        self.disabled = False

    def update_daily_pnl(self, pnl_pct: float) -> None:
        self.daily_pnl_pct = pnl_pct
        if self.daily_pnl_pct <= self.cfg.max_daily_loss_pct:
            self.disabled = True

    def can_open_new(self, equity_usd: float, open_symbol_exposure_pct: float, is_pdt_restricted: bool) -> bool:
        if self.disabled:
            return False
        if open_symbol_exposure_pct >= self.cfg.per_symbol_cap_pct:
            return False
        if is_pdt_restricted:
            return False
        return True