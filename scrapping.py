import requests
from bs4 import BeautifulSoup
import re
import sqlite3

connection = sqlite3.connect('my_books.db')
cursor = connection.cursor()

# Создаем таблицу Books

cursor.execute('''
CREATE TABLE IF NOT EXISTS Books (
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
author TEXT NOT NULL,
pages INTEGER,
price INTEGER,
link TEXT NOT NULL,
genre TEXT NOT NULL,
rating REAL,
image TEXT DEFAULT ''
)
''')
connection.commit()

response = requests.get('https://www.labirint.ru/books/?page=1')
soup = BeautifulSoup(response.text, 'html.parser')




for page_number in range(1, 18):
    response = requests.get(f'https://www.labirint.ru/books/?page={page_number}')
    soup = BeautifulSoup(response.text, 'html.parser')
    product_titles = soup.find('div', class_='body-main-content-wrapper').find_all('a', class_='product-title-link')
    for product in product_titles:
        book_title = product.find('span', class_='product-title').text.strip()  # Получаем название книги
        book_link = product['href']  # Получаем ссылку на книгу

        # Полная ссылка на книгу:
        full_link = f"https://www.labirint.ru{book_link}/?page={page_number}"
        personal_response = requests.get(full_link)
        personal_soup = BeautifulSoup(personal_response.text, 'html.parser')

        # Обработка страниц
        personal_pages = personal_soup.find('div', class_='body-main-content-wrapper').find('div', class_='pages2')
        personal_pages = 0 if personal_pages is None else int(
            re.search(r"(\d+)", personal_pages.text).group(1))  # Обработка отсутствующего атрибута

        # Обработка цены
        personal_price = personal_soup.find('div', class_='body-main-content-wrapper').find('div',
                                                                                            class_='buying-priceold-val').find(
            'span').text

        # Обработка автора
        if personal_soup.find('div', class_='body-main-content-wrapper').find('div', 'authors') is None:
            personal_author = ''
        else:
            if personal_soup.find('div', class_='body-main-content-wrapper').find('div', 'authors').find(
                    'a') is not None:
                personal_author = personal_soup.find('div', class_='body-main-content-wrapper').find('div',
                                                                                                     'authors').find(
                    'a').text
            else:
                personal_author = \
                personal_soup.find('div', class_='body-main-content-wrapper').find('div', 'product-description').find(
                    'div', 'authors').text.split(": ")[1].strip()

        # Обработка жанра
        if len(personal_soup.find('div', class_='body-main-content-wrapper').find('div', id='product').find_all('span',
                                                                                                                class_='thermo-item')) == 2:
            personal_genres = \
            personal_soup.find('div', class_='body-main-content-wrapper').find('div', id='product').find_all('span',
                                                                                                             class_='thermo-item')[
                1].find('span').text
        else:
            personal_genres = \
            personal_soup.find('div', class_='body-main-content-wrapper').find('div', id='product').find_all('span',
                                                                                                             class_='thermo-item')[
                2].find('span').text

        # бработка рейтинга
        personal_rating = float(
            personal_soup.find('div', class_='body-main-content-wrapper').find('div', class_='left').find('div',
                                                                                                          id='rate').text)

        # получение изображения книги
        personal_image = personal_soup.find('div', class_='body-main-content-wrapper').find('div',
                                                                                            id='product-image').find(
            'img').get('data-src')
        cursor.execute(
            'INSERT INTO Books (title, author, pages, price, link, genre,rating,image) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (f'{book_title}', f'{personal_author}', f'{personal_pages}', f'{personal_price}', f'{full_link}',
             f'{personal_genres}', f'{personal_rating}', f'{personal_image}'))

connection.commit()
connection.close()
