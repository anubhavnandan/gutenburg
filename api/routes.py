from flask import request, jsonify, current_app
import psycopg2
from . import config

def get_db_connection():
    conn = psycopg2.connect(
        database=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT
    )
    return conn

@app.route('/books', methods=['GET'])
def get_books():
    query = "SELECT * FROM books WHERE 1=1"
    filters = []

    if 'id' in request.args:
        query += " AND id = %s"
        filters.append(request.args['id'])
    if 'language' in request.args:
        query += " AND language = %s"
        filters.append(request.args['language'])
    if 'mime_type' in request.args:
        query += " AND mime_type = %s"
        filters.append(request.args['mime_type'])
    if 'topic' in request.args:
        query += " AND (subjects LIKE %s OR bookshelves LIKE %s)"
        filters.append('%' + request.args['topic'] + '%')
        filters.append('%' + request.args['topic'] + '%')
    if 'author' in request.args:
        query += " AND author LIKE %s"
        filters.append('%' + request.args['author'] + '%')
    if 'title' in request.args:
        query += " AND title LIKE %s"
        filters.append('%' + request.args['title'] + '%')

    query += " ORDER BY downloads DESC LIMIT 25"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, tuple(filters))
    books = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify({
        "count": len(books),
        "books": books
    })
