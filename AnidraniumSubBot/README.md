# Telegram Subtitle Processing Bot

Автоматизированный Telegram-бот для обработки субтитров и генерации монтажных листов с использованием искусственного интеллекта.

## Возможности

- ✅ Обработка файлов субтитров (SRT, VTT)
- 🤖 Генерация монтажных листов через OpenAI GPT-4
- 📊 Анализ содержимого видео по субтитрам
- 🎬 Профессиональные шаблоны монтажных листов
- ⚡ Асинхронная обработка запросов
- 🔒 Безопасная обработка файлов
- 📝 Подробное логгирование
- 🧪 Полное покрытие тестами

## Быстрый старт

### Установка

```bash
git clone https://github.com/yourusername/telegram_subtitle_bot.git
cd telegram_subtitle_bot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Конфигурация

- Cоздайте `.env` и `config.yaml`, вставьте свои ключи Telegram и OpenAI.

### Запуск

```bash
python main.py
```

## Примеры использования

Скриншоты смотрите в папке `/screenshots`.

1. Запустите бота в Telegram.
2. Отправьте файл субтитров (.srt или .vtt).
3. Получите готовый монтажный лист.

## Документация API

Бот работает только через Telegram API. Вся логика обработки реализована внутри.

## Развертывание

- Поддерживается запуск через Docker, Heroku, любой VPS с Python 3.8+.

## Troubleshooting

- Проверьте правильность токенов и ключей.
- Логи смотрите в файле `bot.log`.
- Для сложных ошибок — создайте Issue.

## Для разработчиков

- Код структурирован по паттерну MVC.
- Все основные сервисы покрыты тестами.
- Для запуска тестов:
  ```bash
  pytest
  ```

## License

MIT

## Контакты

Telegram: @yourusername  
Email: your@email.com