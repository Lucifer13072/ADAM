import openai
from bs4 import BeautifulSoup
import random
import json
import requests
import datetime
from fake_useragent import UserAgent

openai.api_key = "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"



ua = UserAgent()

headers = {
    'accept': 'application/json, text/plain, */*',
    'user-Agent': ua.google,
}

article_dict = {}
links = ['https://habr.com/ru/articles',
         'https://habr.com/ru/articles/page2/',
         'https://habr.com/ru/articles/page3/',
         'https://habr.com/ru/articles/page4/',
         'https://habr.com/ru/articles/page5/']
a = 0
for i in links:
    req = requests.get(i, headers=headers).text

    soup = BeautifulSoup(req, 'lxml')
    all_hrefs_articles = soup.find_all('a', class_='tm-title__link') # получаем статьи
    for article in all_hrefs_articles: # проходимся по статьям
        a += 1
        article_name = article.find('span').text # собираем названия статей
        article_link = f'https://habr.com{article.get("href")}' # ссылки на статьи
        article_dict[article_name] = article_link
        article_dict[a] = article_link

    with open(f"data/states_Hubr.json", "w", encoding='utf-8') as f: 
        try:    
            json.dump(article_dict, f, indent=4, ensure_ascii=False)
            print('Статьи были успешно получены')
        except:
            print('Статьи не удалось получить')
