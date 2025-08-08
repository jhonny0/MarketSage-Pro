from __future__ import annotations

from typing import Optional

from telegram import Bot


class TelegramNotifier:
    def __init__(self, bot_token: Optional[str], chat_id: Optional[str]) -> None:
        self.enabled = bool(bot_token and chat_id)
        self.bot = Bot(bot_token) if self.enabled else None
        self.chat_id = chat_id

    async def send(self, text: str) -> None:
        if not self.enabled or not self.bot or not self.chat_id:
            return
        await self.bot.send_message(chat_id=self.chat_id, text=text)