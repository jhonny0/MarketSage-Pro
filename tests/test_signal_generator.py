from market_sage_pro.signals.generator import SignalConfig, generate_signal


def test_signal_buy_option():
    cfg = SignalConfig(kelly_fraction_cap=0.5)
    sig = generate_signal(
        ensemble_up_prob=0.75,
        ensemble_down_prob=0.25,
        predicted_move_pct=0.3,
        rsi=50,
        price_vs_ema21=1,
        ivr=0.2,
        prob_big_move=0.7,
        cfg=cfg,
    )
    assert sig.action in ("OPTION_SELL_STRADDLE", "OPTION_BUY_ATM")
    assert 0 <= sig.size_fraction <= 0.5
    assert 0 <= sig.confidence <= 100


def test_signal_hold():
    cfg = SignalConfig(kelly_fraction_cap=0.5)
    sig = generate_signal(
        ensemble_up_prob=0.5,
        ensemble_down_prob=0.5,
        predicted_move_pct=0.0,
        rsi=50,
        price_vs_ema21=0.0,
        ivr=0.5,
        prob_big_move=0.5,
        cfg=cfg,
    )
    assert sig.action == "HOLD"