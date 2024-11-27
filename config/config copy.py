import os
import ssl
from dataclasses import dataclass
from typing import List, Dict, Union, Optional, Any
from dotenv import load_dotenv

load_dotenv()

# Telegram Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
ADMIN_IDS = list(map(int, os.getenv('ADMIN_IDS', '').split(',')))

# Google AI Configuration
GOOGLE_AI_API_KEY = os.getenv('GOOGLE_AI_API_KEY')

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL')

# Scraping Configuration
SCRAPING_INTERVAL = int(os.getenv('SCRAPING_INTERVAL', '3600'))
MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '30'))
CONCURRENT_REQUESTS = int(os.getenv('CONCURRENT_REQUESTS', '3'))

def create_lenient_ssl_context():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context


@dataclass
class MedicalSource:
    name: str
    url: str
    category: List[str]
    language: str
    selectors: Dict[str, Union[str, List[str]]]
    headers: Optional[Dict[str, str]] = None
    requires_js: bool = False
    pagination: Optional[Dict[str, str]] = None
    ssl_context: Optional[ssl.SSLContext] = None
    verify_ssl: bool = True  

# Существующие источники остаются без изменений
MEDICAL_SOURCES = [
    MedicalSource(
        name="Ya Roditel",
        url="https://www.ya-roditel.ru/parents/base/experts/",
        category=["parenting"],
        language="ru",
        selectors={
            'article': ['a.post__img ', 'div.article-item', '.articles-list__item'],
            'title': ['a','div.post__title','a.post__title' ,'post__title','h2.title', '.article-title'],
            'content': ['div.post__description', '.article-text', '.content-text'],
            'link': ['a.post__title', 'a.article-title', 'h2.title a']
        },
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    ),
    
    MedicalSource(
        name="downsideup",
        url="https://downsideup.org/o-fonde/novosti/",
        category=["news","parenting","social-support"],
        language="ru",
        selectors = {
            'article': ['.post', 'article', '.blog-post', 'div.entry', '.news-item'],
            'title': ['h4','h4.link link_blue','title','h4.title','h1', 'h2', '.entry-title', 'a.post-title', '.title', 'div.title'],
            'content': ['.entry-content', 'div.content', 'article p', '.post-text', 'p'],
            'link': ['a', 'a.post-title', 'h1 a', 'h2 a', '.read-more']
        },
        requires_js=True,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
        }
    ),

    MedicalSource(
        name="РООИ Перспектива",
        url="https://perspektiva-inva.ru/news",
        category=["social-support", "rehabilitation"],
        language="ru",
        selectors={
            'article': ['.post', 'article', 'div.news', '.news-item', '.content-block'],
            'title': ['h1', 'h2', '.title', 'a.news-title', 'div.title'],
            'content': ['.entry-content', 'div.text', 'article p', 'p', '.content'],
            'link': ['a', 'a.news-title', 'h1 a', 'h2 a', '.read-more']
        }
    ),
    MedicalSource(
        name="Форум Особые дети",
        url="https://specialchildren.livejournal.com",
        category=["parenting", "support", "experience"],
        language="ru",
        selectors={
            'article': ['div.entry', 'div.post', 'article', '.entry', 'section', 'div'],
            'title': ['h1', 'h2', 'h3', '.title', 'div.subject', 'a.subject', 'div', 'h1 a'],
            'content': ['.entry-text', 'div.text', 'article p', 'p', 'div', '.content'],
            'link': ['a.subject', 'h1 a', 'h2 a', '.entry-link', 'a']
        },
        requires_js=True,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    )
]


# Существующие промпты и константы остаются без изменений
CONTENT_PROMPTS = {
    'research': """
    {emoji} {title}

    {content}

    🔬 Ключевые результаты исследования:
    {key_points}

    💡 Практическое значение:
    {practical_application}

    🌐 Источник: [{source}]

    {tags}"""
}

AI_GENERATION_PROMPTS = {
    'advice': """
Создайте профессиональный медицинский пост-совет на тему {category}:

Заголовок: [Краткий, привлекательный заголовок]

Основное содержание: 
Напишите 2-3 развернутых абзаца о теме. Используйте понятный язык, избегайте сложных медицинских терминов. Объясните суть проблемы и подходы к ее решению.

Ключевые моменты:
- Первый ключевой момент - краткое и емкое утверждение
- Второй ключевой момент - практический совет
- Третий ключевой момент - важное предостережение

Практическое применение: 
Напишите конкретные рекомендации, которые читатель может применить сразу же. Сделайте их максимально praktичными и понятными.

Обязательно используйте:
- Простой, понятный язык
- Конкретные примеры
- Практические советы

Теги: #здоровье #совет #медицина
""",
}


POST_TEMPLATES = {
    'default': """
{emoji} {title}

{content}

🔑 Ключевые моменты:
{key_points}

💡 Практическое значение:
{practical_application}

🌐 Источник: [{source}]({source_url})

{tags}""",
    'research': """
{title}

{content}

🔬 Ключевые результаты исследования:
{key_points}

💡 Практическое значение:
{practical_application}

🌐 Источник: [{source}]

{tags}"""
}