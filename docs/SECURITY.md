# Security Notes

- Secrets are stored encrypted using `python-gnupg` symmetric encryption.
- `config.yaml` is not committed; `secrets.gpg` holds encrypted values.
- Decryption only occurs in-process at launch using a passphrase.
- Avoid printing secrets in logs. Never write decrypted secrets to disk.
- Consider moving to a dedicated secret manager (e.g., AWS KMS, HashiCorp Vault) for production.