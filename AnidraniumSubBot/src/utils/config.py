"""
Управление конфигурацией приложения.
"""

import os
from dataclasses import dataclass
import yaml
from dotenv import load_dotenv

@dataclass
class Config:
    telegram_token: str
    openai_api_key: str
    log_level: str = "INFO"
    max_file_size: int = 20 * 1024 * 1024
    templates_dir: str = "templates"
    cache_ttl: int = 3600
    rate_limit_requests: int = 5
    rate_limit_window: int = 60

def load_config() -> Config:
    load_dotenv()
    with open("config.yaml", "r", encoding="utf-8") as f:
        yml = yaml.safe_load(f)
    return Config(
        telegram_token=os.getenv("TELEGRAM_TOKEN", yml.get("telegram_token")),
        openai_api_key=os.getenv("OPENAI_API_KEY", yml.get("openai_api_key")),
        log_level=os.getenv("LOG_LEVEL", yml.get("log_level", "INFO")),
        max_file_size=int(os.getenv("MAX_FILE_SIZE", yml.get("max_file_size", 20971520))),
        templates_dir=os.getenv("TEMPLATES_DIR", yml.get("templates_dir", "templates")),
        cache_ttl=int(os.getenv("CACHE_TTL", yml.get("cache_ttl", 3600))),
        rate_limit_requests=int(os.getenv("RATE_LIMIT_REQUESTS", yml.get("rate_limit_requests", 5))),
        rate_limit_window=int(os.getenv("RATE_LIMIT_WINDOW", yml.get("rate_limit_window", 60))),
    )