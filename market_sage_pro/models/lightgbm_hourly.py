from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np

try:
    import lightgbm as lgb
except Exception:  # pragma: no cover - fallback if not installed
    lgb = None  # type: ignore


@dataclass
class HourlyModelConfig:
    num_leaves: int = 31
    learning_rate: float = 0.05
    n_estimators: int = 200
    random_state: int = 42


class HourlyLightGBM:
    def __init__(self, cfg: Optional[HourlyModelConfig] = None) -> None:
        self.cfg = cfg or HourlyModelConfig()
        self.model = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        if lgb is None:
            self.model = (X.mean(), y.mean())  # trivial fallback
            return
        self.model = lgb.LGBMClassifier(
            num_leaves=self.cfg.num_leaves,
            learning_rate=self.cfg.learning_rate,
            n_estimators=self.cfg.n_estimators,
            random_state=self.cfg.random_state,
        )
        self.model.fit(X, y)

    def partial_update(self, X: np.ndarray, y: np.ndarray) -> None:
        # retrain simple approach; in production use DART/keep booster
        self.fit(X, y)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if self.model is None:
            return np.full((X.shape[0], 2), 0.5)
        if lgb is None:
            _, y_mean = self.model
            proba = np.clip(y_mean, 0.01, 0.99)
            return np.column_stack([1 - proba, proba])
        return self.model.predict_proba(X)