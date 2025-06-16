"""
Тесты для основных функций Telegram-бота.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from telegram import Update, Document, User, Chat, Message
from telegram.ext import ContextTypes

from src.bot.handlers import BotHandlers
from src.services.ai_service import AIService

@pytest.mark.asyncio
async def test_start_handler():
    config = MagicMock()
    handler = BotHandlers(config)
    update = MagicMock(spec=Update)
    context = MagicMock()
    update.message = MagicMock()
    await handler.start_handler(update, context)
    update.message.reply_text.assert_called_with("Привет! Пришли мне субтитры (SRT/VTT), и я создам монтажный лист.")