import math
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.append(str(Path(__file__).resolve().parents[2]))

from market_sage_pro.backtest.engine import backtest
from market_sage_pro.signals.generator import SignalConfig


def test_backtest_metrics() -> None:
    idx = pd.date_range('2023-01-01', periods=2, freq='B')
    df = pd.DataFrame({
        'p_up': [0.8, 0.2],
        'p_down': [0.2, 0.8],
        'pred_move': [0.5, -0.5],
        'rsi': [50, 50],
        'px_vs_ema21': [0.1, -0.1],
        'ivr': [0.5, 0.5],
        'p_big': [0.7, 0.7],
        'actual_move': [1.0, -0.5],
    }, index=idx)

    res = backtest(df, SignalConfig(kelly_fraction_cap=0.5))

    assert res['trades'] == 2
    assert res['win_rate'] == 0.5
    assert res['equity'] == pytest.approx(1.00238848, rel=1e-6)
    assert res['max_drawdown'] == pytest.approx(0.0024, abs=1e-6)
    assert res['profit_factor'] == pytest.approx(2.0, rel=1e-6)
    assert math.isnan(res['Sortino'])
