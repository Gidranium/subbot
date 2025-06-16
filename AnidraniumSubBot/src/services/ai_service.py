"""
Сервис для работы с OpenAI API и генерации монтажных листов.
"""

import asyncio
import logging
import openai
from openai import AsyncOpenAI
import hashlib

SYSTEM_PROMPT_TEMPLATE = """
Ты профессиональный видеомонтажер и помощник по созданию монтажных листов.
Твоя задача - проанализировать субтитры видео и создать детальный монтажный лист.

ПРАВИЛА:
1. Анализируй диалоги и определяй ключевые сцены
2. Создавай структурированный монтажный лист с тайм-кодами
3. Включай описания действий и переходов
4. Следуй формату предоставленного шаблона
5. Используй профессиональную терминологию

ШАБЛОН ДЛЯ СЛЕДОВАНИЯ:
{template}

ФОРМАТ ОТВЕТА:
- Возвращай только готовый монтажный лист
- Не добавляй комментарии или объяснения
- Соблюдай структуру шаблона
"""

class AIService:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.cache = {}

    async def analyze_subtitles(self, content: str, template: str) -> str:
        cache_key = self._cache_key(content + template)
        if cache_key in self.cache:
            logging.info("AIService: returning cached result")
            return self.cache[cache_key]

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT_TEMPLATE.format(template=template)},
            {"role": "user", "content": content}
        ]
        try:
            response = await self._make_request_with_retry(messages)
            self.cache[cache_key] = response
            return response
        except Exception as e:
            logging.error(f"AIService error: {e}")
            return "Ошибка анализа субтитров AI."

    async def _make_request_with_retry(self, messages, retries=3, delay=2):
        for attempt in range(retries):
            try:
                resp = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.3,
                    max_tokens=2048,
                )
                result = resp.choices[0].message.content.strip()
                if self._validate_response(result):
                    return result
            except openai.RateLimitError as e:
                await asyncio.sleep(delay * (2 ** attempt))
            except Exception as e:
                logging.error(f"AIService request error: {e}")
                break
        raise Exception("AIService: all retries failed")

    def _validate_response(self, response: str) -> bool:
        return bool(response and len(response) > 10)

    def _cache_key(self, content: str) -> str:
        return hashlib.sha256(content.encode()).hexdigest()