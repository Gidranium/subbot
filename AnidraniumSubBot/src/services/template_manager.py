"""
Менеджер шаблонов для создания монтажных листов.
"""

import os
import logging

DEFAULT_TEMPLATE = """
МОНТАЖНЫЙ ЛИСТ

Название: {project_name}
Дата: {date}
Длительность: {duration}

СТРУКТУРА СЦЕН:

{scenes}

ТЕХНИЧЕСКИЕ ПРИМЕЧАНИЯ:

{technical_notes}
"""

class TemplateManager:
    def __init__(self, templates_dir: str):
        self.templates_dir = templates_dir
        self.templates = {"default": DEFAULT_TEMPLATE}
        self.load_templates()

    def load_templates(self):
        # Подгрузить кастомные шаблоны из директории
        for fname in os.listdir(self.templates_dir):
            if fname.endswith(".txt"):
                with open(os.path.join(self.templates_dir, fname), 'r', encoding='utf-8') as f:
                    self.templates[fname.rsplit('.', 1)[0]] = f.read()

    def get_template(self, template_name: str = "default") -> str:
        return self.templates.get(template_name, DEFAULT_TEMPLATE)

    def list_available_templates(self):
        return list(self.templates.keys())

    def validate_template(self, template_content: str) -> bool:
        # Простейшая валидация
        return "{scenes}" in template_content

    def reload_templates(self):
        self.load_templates()