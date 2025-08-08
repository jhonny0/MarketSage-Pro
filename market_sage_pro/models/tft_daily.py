from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass
class DailyTFTConfig:
    dummy: int = 0


class DailyTFT:
    def __init__(self, cfg: Optional[DailyTFTConfig] = None) -> None:
        self.cfg = cfg or DailyTFTConfig()

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        # Placeholder: no-op
        return

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        # Placeholder uniform probability
        return np.full((X.shape[0], 2), 0.5)