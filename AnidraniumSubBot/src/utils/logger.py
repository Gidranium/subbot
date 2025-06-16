"""
Конфигурация системы логгирования приложения.
"""

import logging
import logging.handlers
import sys
import json

def setup_logging(log_level: str = "INFO", log_file: str = "bot.log"):
    handler = logging.handlers.TimedRotatingFileHandler(log_file, when="midnight", backupCount=7, encoding="utf-8")
    console = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "msg": "%(message)s"}'
    )
    handler.setFormatter(formatter)
    console.setFormatter(formatter)
    logging.basicConfig(
        level=getattr(logging, log_level),
        handlers=[handler, console]
    )