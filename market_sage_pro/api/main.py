from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from typing import Annotated

import orjson
from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ..backtest.engine import run_backtest
from ..config import AppConfig, load_config
from ..signals.generator import SignalConfig, generate_signal


class ORJSONResponse:
    media_type = "application/json"

    def __init__(self, content: object) -> None:
        self.body = orjson.dumps(content)


def get_settings() -> AppConfig:
    path = "config.yaml" if __import__("os").path.exists("config.yaml") else "config.yaml.example"
    return load_config(path)


app = FastAPI(title="MarketSage-Pro API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SignalRequest(BaseModel):
    ensemble_up_prob: float
    ensemble_down_prob: float
    predicted_move_pct: float
    rsi: float
    price_vs_ema21: float
    ivr: float
    prob_big_move: float


class BacktestRequest(BaseModel):
    from_date: str
    to_date: str
    symbols: list[str]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/signal")
def post_signal(req: SignalRequest, cfg: Annotated[AppConfig, Depends(get_settings)]) -> dict[str, object]:
    sig = generate_signal(
        ensemble_up_prob=req.ensemble_up_prob,
        ensemble_down_prob=req.ensemble_down_prob,
        predicted_move_pct=req.predicted_move_pct,
        rsi=req.rsi,
        price_vs_ema21=req.price_vs_ema21,
        ivr=req.ivr,
        prob_big_move=req.prob_big_move,
        cfg=SignalConfig(kelly_fraction_cap=cfg.kelly_fraction_cap),
    )
    return sig.__dict__


@app.post("/backtest")
def post_backtest(req: BacktestRequest) -> Mapping[str, object]:
    try:
        start = datetime.fromisoformat(req.from_date)
        end = datetime.utcnow() if req.to_date.lower() == "today" else datetime.fromisoformat(req.to_date)
    except ValueError:
        return {"error": "invalid date"}
    res = run_backtest(req.symbols, start, end)
    return res


@app.websocket("/ws/stream")
async def ws_stream(ws: WebSocket) -> None:
    await ws.accept()
    try:
        await ws.send_json({"msg": "stream started"})
        # Placeholder: in production, push live ticks/minute bars
        while True:
            data = await ws.receive_text()
            await ws.send_json({"echo": data})
    except WebSocketDisconnect:
        pass