## Architecture

- Data Feed: Polygon WS primary, IEX/Yahoo fallback (stubs provided)
- Storage: DuckDB per symbol, 180-day retention
- Features: EMA/RSI/MACD/ATR/VWAP + placeholders for orderflow/options/sentiment
- Models: LightGBM hourly (online retrain) + TFT daily (stub), MLflow registry
- Signals: Rule-based thresholds + options logic + Kelly sizing
- Risk: Daily loss circuit breaker, per-symbol cap, PDT throttle
- Backtest: Simple engine + metrics; Optuna (placeholder) for tuning
- UI: React + Vite + Tailwind single page
- Infra: FastAPI API, APScheduler, Redis, Docker Compose, GitHub Actions CI