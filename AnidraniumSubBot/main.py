"""
Telegram Bot для обработки субтитров и генерации монтажных листов.
Author: AI Assistant
Version: 1.0.0
"""

import asyncio
import logging
import os
import signal
from pathlib import Path

from telegram.ext import Application
from dotenv import load_dotenv

from src.bot.handlers import BotHandlers
from src.bot.middleware import RateLimitingMiddleware
from src.utils.logger import setup_logging
from src.utils.config import load_config

class TelegramBot:
    def __init__(self, token: str, config):
        self.token = token
        self.config = config
        self.app = Application.builder().token(token).build()
        self.handlers = BotHandlers(config)
        self.setup_handlers()
        self.app.add_middleware(RateLimitingMiddleware(config))

    def setup_handlers(self):
        self.handlers.register(self.app)

    async def run(self):
        logging.info("Bot started")
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()
        await self._setup_signals()
        await self.app.updater.idle()

    async def shutdown(self):
        logging.info("Bot is shutting down...")
        await self.app.updater.stop()
        await self.app.stop()
        await self.app.shutdown()
        logging.info("Shutdown complete.")

    async def _setup_signals(self):
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda: asyncio.create_task(self.shutdown()))

def main():
    setup_logging()
    load_dotenv()
    config = load_config()
    bot = TelegramBot(config.telegram_token, config)
    try:
        asyncio.run(bot.run())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped by user.")

if __name__ == "__main__":
    main()