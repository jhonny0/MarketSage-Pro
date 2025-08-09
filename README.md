# MarketSage-Pro

Personal trading copilot for U.S. equities and options. Streams real-time data, predicts next-hour/next-day moves, and surfaces trade setups with strict risk controls.

No Financial Advice. Trade at Your Own Risk.

## Quick start (≤ 10 min)

1) Install prerequisites
- Python 3.10+
- Node 18+
- Docker + Docker Compose

2) Copy config
```bash
cp config.yaml.example config.yaml
```
Fill `alpaca_key/secret` and optionally `alpaca_endpoint` (default `https://paper-api.alpaca.markets/v2`), `max_daily_loss_pct`, `kelly_fraction_cap`, optional `telegram_bot_token/chat_id`.

3) Run services
```bash
docker compose up --build
```
API: http://localhost:8000
UI: http://localhost:5173

4) First signal path
- UI defaults to Paper mode. Switch to Live in the Control Center toggle (top-right) once ready.
- Signals begin populating when `alpaca_key/secret` are set and the U.S. market is open.
- Screenshot placeholder: docs/img/dashboard.png

5) Backtest example
```bash
python -m market_sage_pro.backtest.engine --from 2023-01-01 --to today --symbols AAPL,MSFT
```

## 🔐 Encrypt your config
We encrypt API keys using symmetric GPG via python-gnupg.

- One-time: encrypt your `config.yaml` secrets into `secrets.gpg` with a passphrase
```bash
python -c "from market_sage_pro.config import load_config, ensure_encrypted_secrets; ensure_encrypted_secrets(load_config('config.yaml'), passphrase='YOUR_STRONG_PASSPHRASE')"
```
- At runtime, the app can decrypt in-process using the same passphrase (see `market_sage_pro.config.decrypt_secrets`). Keep the passphrase out of logs and source control.
- Optional (not required for symmetric encryption): you may still generate a GPG keypair via `gpg --full-generate-key` for your own workflows.

## Health checks & dependencies
Services have container health checks to fail fast:
- api: GET `/health` must return `{status: "ok"}`
- scheduler: must successfully ping Redis
See `docker-compose.yml` for details.

## Running tests
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=$(pwd) pytest -q --cov=market_sage_pro --cov-report=term-missing
```
Target coverage ≥ 85% (CI enforces threshold; raise locally as modules mature).

## Back-test output
Metrics printed include: CAGR, Max Drawdown, Sharpe, Sortino, Win-rate, Profit-factor, Trades, Equity. Use these to compare against SPY’s risk-adjusted return and max DD targets.

## Model tracking (MLflow)
- Tracking URI defaults to `file:./mlruns`
- Launch UI locally:
```bash
mlflow ui --backend-store-uri ./mlruns --port 5000
```
Open http://localhost:5000 to browse experiments.

## Notifications
- Telegram: create a bot with BotFather, obtain `telegram_bot_token` and your `telegram_chat_id`, and set them in `config.yaml`. Signals and circuit-breakers can push alerts.
- Daily PDF performance report is rendered with WeasyPrint and saved to `reports/`.

## API collection & demos
- Postman collection: `docs/api.postman_collection.json`
- Notebook demos: see `notebooks/` (advanced tinkering)

## Disclaimers & compliance
- No Financial Advice. Trade at Your Own Risk.
- Pattern Day Trader (PDT) rule: if equity < $25,000, day trading activity may be limited; the app throttles when appropriate.

## Services
- api: FastAPI + WebSocket for live data, signals, and REST control
- scheduler: APScheduler + Redis queue for periodic jobs (training, backtests, reports)
- ui: React + Vite + Tailwind single-page dashboard

## Features
- Redundant data feeds (Polygon WS primary, IEX/Yahoo fallback)
- DuckDB local store (rolling 180 days per symbol)
- Technical + order-flow + options + sentiment features
- Prediction: LightGBM (hourly, online) and TFT (daily) with MLflow registry
- Signal generation with options plays and risk-based sizing
- Risk & compliance guardrails
- Backtest & walk-forward with Optuna tuning
- Notifications: Telegram/email; daily PDF report

See `docs/` for more details.