from market_sage_pro.risk.manager import RiskConfig, RiskManager


def test_risk_manager_circuit_breaker():
    rm = RiskManager(RiskConfig(max_daily_loss_pct=-2))
    assert rm.can_open_new(100000, 0, False)
    rm.update_daily_pnl(-3)
    assert not rm.can_open_new(100000, 0, False)


def test_risk_manager_per_symbol_cap():
    rm = RiskManager(RiskConfig(max_daily_loss_pct=-2))
    assert not rm.can_open_new(100000, 5.0, False)


def test_risk_manager_pdt_equity_check():
    rm = RiskManager(RiskConfig(max_daily_loss_pct=-2))
    # Equity below $25k should prevent opening new positions even if the
    # caller forgets to set is_pdt_restricted.
    assert not rm.can_open_new(24_000, 0, False)