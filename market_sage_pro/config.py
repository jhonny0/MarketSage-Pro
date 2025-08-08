from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field, ValidationError, field_validator

from .secrets import decrypt_text, encrypt_text
from .utils.logging import get_logger

logger = get_logger(__name__)


class AppConfig(BaseModel):
    alpaca_key: str
    alpaca_secret: str
    max_daily_loss_pct: float = Field(..., le=0)
    kelly_fraction_cap: float = Field(..., ge=0, le=1)
    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None
    polygon_api_key: str | None = None
    iex_api_key: str | None = None
    openai_api_key: str | None = None
    gpg_home: str | None = None

    @field_validator("max_daily_loss_pct")
    @classmethod
    def check_negative(cls, v: float) -> float:
        if v > 0:
            raise ValueError("max_daily_loss_pct must be <= 0 (e.g., -2)")
        return v


@dataclass
class SecretBundle:
    alpaca_key_enc: bytes
    alpaca_secret_enc: bytes
    openai_api_key_enc: Optional[bytes]
    polygon_api_key_enc: Optional[bytes]
    iex_api_key_enc: Optional[bytes]


def load_config(path: str = "config.yaml") -> AppConfig:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    try:
        cfg = AppConfig(**data)
    except ValidationError as e:
        raise RuntimeError(f"Invalid config.yaml: {e}")
    return cfg


def ensure_encrypted_secrets(cfg: AppConfig, passphrase: str, secrets_path: str = "secrets.gpg") -> None:
    if Path(secrets_path).exists():
        logger.info("Encrypted secrets already exist; skipping re-encryption.")
        return
    logger.info("Encrypting secrets to secrets.gpg")
    bundle = SecretBundle(
        alpaca_key_enc=encrypt_text(cfg.alpaca_key, passphrase, cfg.gpg_home),
        alpaca_secret_enc=encrypt_text(cfg.alpaca_secret, passphrase, cfg.gpg_home),
        openai_api_key_enc=encrypt_text(cfg.openai_api_key or "", passphrase, cfg.gpg_home)
        if cfg.openai_api_key
        else None,
        polygon_api_key_enc=encrypt_text(cfg.polygon_api_key or "", passphrase, cfg.gpg_home)
        if cfg.polygon_api_key
        else None,
        iex_api_key_enc=encrypt_text(cfg.iex_api_key or "", passphrase, cfg.gpg_home)
        if cfg.iex_api_key
        else None,
    )
    # Simple YAML binary dump
    dump = {
        "alpaca_key": bundle.alpaca_key_enc.decode("utf-8"),
        "alpaca_secret": bundle.alpaca_secret_enc.decode("utf-8"),
        "openai_api_key": bundle.openai_api_key_enc.decode("utf-8") if bundle.openai_api_key_enc else "",
        "polygon_api_key": bundle.polygon_api_key_enc.decode("utf-8") if bundle.polygon_api_key_enc else "",
        "iex_api_key": bundle.iex_api_key_enc.decode("utf-8") if bundle.iex_api_key_enc else "",
    }
    with open(secrets_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(dump, f)


def decrypt_secrets(passphrase: str, cfg: AppConfig, secrets_path: str = "secrets.gpg") -> dict[str, str]:
    if not Path(secrets_path).exists():
        raise FileNotFoundError("secrets.gpg not found. Run initial encryption.")
    with open(secrets_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    out: dict[str, str] = {}
    for key in ["alpaca_key", "alpaca_secret", "openai_api_key", "polygon_api_key", "iex_api_key"]:
        enc = data.get(key, "")
        if not enc:
            continue
        out[key] = decrypt_text(enc.encode("utf-8"), passphrase, cfg.gpg_home)
    return out