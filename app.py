from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


def get_books(sort_by=None, order='asc', search=''):
    # Подключение к базе данных
    conn = sqlite3.connect('my_books.db')
    cursor = conn.cursor()

    # Формирование SQL-запроса с учетом сортировки и поиска
    query = "SELECT * FROM Books"
    filters = []

    if search:
        filters.append(f"Title LIKE ?")

    if filters:
        query += " WHERE " + " AND ".join(filters)

    if sort_by:
        query += f" ORDER BY {sort_by} {'ASC' if order == 'asc' else 'DESC'}"

    params = [f'%{search}%'] if search else []
    cursor.execute(query, params)
    books = cursor.fetchall()  # Извлекаем все записи
    conn.close()  # Закрываем соединение
    return books


@app.route("/", methods=["GET"])
def index():
    sort_by = request.args.get('sort_by')  # Получаем параметр сортировки из URL
    order = request.args.get('order', 'asc')  # Получаем порядок сортировки
    search = request.args.get('search', '')  # Получаем поисковый запрос
    books = get_books(sort_by, order, search)  # Получаем книги из базы данных с учетом сортировки и поиска
    return render_template("index.html", books=books, current_order=order, current_search=search)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
