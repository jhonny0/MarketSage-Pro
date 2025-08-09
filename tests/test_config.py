import os
import tempfile

import pytest

from market_sage_pro.config import AppConfig, ensure_encrypted_secrets, decrypt_secrets


def test_app_config_validation():
    cfg = AppConfig(
        alpaca_key="k",
        alpaca_secret="s",
        max_daily_loss_pct=-2,
        kelly_fraction_cap=0.5,
    )
    assert cfg.max_daily_loss_pct == -2
    assert cfg.alpaca_endpoint == "https://paper-api.alpaca.markets/v2"

    with pytest.raises(Exception):
        AppConfig(
            alpaca_key="k",
            alpaca_secret="s",
            max_daily_loss_pct=1,
            kelly_fraction_cap=0.5,
        )


def test_secrets_encrypt_decrypt(tmp_path):
    import shutil, pytest
    if shutil.which("gpg") is None:
        pytest.skip("gpg binary not available; skipping encryption test")
    cfg = AppConfig(
        alpaca_key="k",
        alpaca_secret="s",
        max_daily_loss_pct=-2,
        kelly_fraction_cap=0.5,
        gpg_home=str(tmp_path / ".gnupg"),
    )
    secrets_path = tmp_path / "secrets.gpg"
    ensure_encrypted_secrets(cfg, passphrase="pass", secrets_path=str(secrets_path))
    out = decrypt_secrets(passphrase="pass", cfg=cfg, secrets_path=str(secrets_path))
    assert out["alpaca_key"] == "k"
    assert out["alpaca_secret"] == "s"