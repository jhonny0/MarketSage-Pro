from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import gnupg


def _get_gpg(gpg_home: str | None = None) -> gnupg.GPG:
    home = gpg_home or os.environ.get("GPG_HOME") or ".gnupg"
    Path(home).mkdir(parents=True, exist_ok=True)
    return gnupg.GPG(gnupghome=home)


def encrypt_text(plaintext: str, passphrase: str, gpg_home: Optional[str] = None) -> bytes:
    gpg = _get_gpg(gpg_home)
    result = gpg.encrypt(plaintext, recipients=None, symmetric=True, passphrase=passphrase)
    if not result.ok:
        raise RuntimeError(f"Encryption failed: {result.status}")
    return bytes(str(result), "utf-8")


def decrypt_text(ciphertext: bytes, passphrase: str, gpg_home: Optional[str] = None) -> str:
    gpg = _get_gpg(gpg_home)
    result = gpg.decrypt(ciphertext, passphrase=passphrase)
    if not result.ok:
        raise RuntimeError(f"Decryption failed: {result.status}")
    return str(result)