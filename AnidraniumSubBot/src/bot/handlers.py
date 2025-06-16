"""
Обработчики событий Telegram-бота для работы с субтитрами.
"""

import logging
from telegram import Update, Document
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

from ..services.ai_service import AIService
from ..services.subtitle_parser import SubtitleParser
from ..services.template_manager import TemplateManager
from ..utils.file_handler import FileHandler

class BotHandlers:
    def __init__(self, config):
        self.config = config
        self.ai_service = AIService(config.openai_api_key)
        self.subtitle_parser = SubtitleParser()
        self.template_manager = TemplateManager(config.templates_dir)
        self.file_handler = FileHandler(config.max_file_size)

    def register(self, app):
        app.add_handler(CommandHandler("start", self.start_handler))
        app.add_handler(CommandHandler("help", self.help_handler))
        app.add_handler(MessageHandler(filters.Document.ALL, self.document_handler))
        app.add_handler(MessageHandler(filters.TEXT, self.text_handler))

    async def start_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            await update.message.reply_text("Привет! Пришли мне субтитры (SRT/VTT), и я создам монтажный лист.")
        except Exception as e:
            logging.error(f"Error in start_handler: {e}")

    async def help_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = (
            "Этот бот принимает файлы субтитров (.srt, .vtt) и генерирует монтажный лист.\n"
            "Отправьте файл субтитров — получите результат!"
        )
        await update.message.reply_text(help_text)

    async def document_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            document: Document = update.message.document
            if not self.file_handler.is_valid(document):
                await update.message.reply_text("Файл должен быть SRT или VTT, размер ≤ 20MB.")
                return
            await update.message.reply_text("Обрабатываю файл...")
            file_path = await self.file_handler.download(document, context)
            entries = self.subtitle_parser.parse_file(file_path)
            stats = self.subtitle_parser.get_statistics(entries)
            ai_input = self.subtitle_parser.format_for_ai(entries)
            template = self.template_manager.get_template()
            result = await self.ai_service.analyze_subtitles(ai_input, template)
            await update.message.reply_text("Монтажный лист готов!\n\n" + result)
        except Exception as e:
            logging.error(f"Error in document_handler: {e}")
            await update.message.reply_text("Произошла ошибка при обработке файла. Попробуйте позже.")

    async def text_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Пожалуйста, отправьте файл субтитров в формате .srt или .vtt.")