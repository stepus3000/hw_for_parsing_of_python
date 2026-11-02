import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

## Определяем список ключевых слов:
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

## Ваш код
URL = 'https://habr.com/ru/articles/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/124.0 Safari/537.36'}

response = requests.get(URL, headers=HEADERS, timeout=10)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

for article in soup.select('article.tm-articles-list__item'):
    title_tag = article.select_one('h2.tm-title a.tm-title__link')
    time_tag = article.select_one('time')
    if title_tag is None or time_tag is None:
        continue

    title = title_tag.get_text(strip=True)
    link = urljoin(URL, title_tag['href'])
    # В тексте тега "3 часа назад", а точная дата лежит в атрибуте datetime
    date = time_tag.get('datetime', '')[:16].replace('T', ' ')

    # Вся preview-информация: заголовок + текст анонса + названия хабов
    preview_tag = article.select_one('.article-formatted-body')
    preview = preview_tag.get_text(' ', strip=True) if preview_tag else ''
    hubs = ' '.join(h.get_text(strip=True)
                    for h in article.select('.tm-publication-hub__link'))

    text = f'{title} {preview} {hubs}'.lower()

    if any(keyword.lower() in text for keyword in KEYWORDS):
        print(f'{date} – {title} – {link}')
