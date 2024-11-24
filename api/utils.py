import psycopg2
from psycopg2.extras import RealDictCursor
from .config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def get_db_connection():
    """
    Establish and return a connection to the PostgreSQL database.
    """
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        cursor_factory=RealDictCursor  # This allows fetching rows as dictionaries
    )
    return conn

def fetch_books(filters):
    """
    Fetch books from the database based on the provided filters.
    """
    query = "SELECT * FROM books WHERE 1=1"
    query_filters = []

    if 'id' in filters:
        query += " AND id = %s"
        query_filters.append(filters['id'])
    if 'language' in filters:
        query += " AND language = %s"
        query_filters.append(filters['language'])
    if 'mime_type' in filters:
        query += " AND mime_type = %s"
        query_filters.append(filters['mime_type'])
    if 'topic' in filters:
        query += " AND (subjects LIKE %s OR bookshelves LIKE %s)"
        query_filters.append('%' + filters['topic'] + '%')
        query_filters.append('%' + filters['topic'] + '%')
    if 'author' in filters:
        query += " AND author LIKE %s"
        query_filters.append('%' + filters['author'] + '%')
    if 'title' in filters:
        query += " AND title LIKE %s"
        query_filters.append('%' + filters['title'] + '%')

    query += " ORDER BY downloads DESC LIMIT 25"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, tuple(query_filters))
    books = cursor.fetchall()
    cursor.close()
    conn.close()

    return books

def format_books(books):
    """
    Format the books data into the desired JSON structure.
    """
    formatted_books = []
    for book in books:
        formatted_book = {
            "title": book['title'],
            "author": book['author'],
            "genre": book['genre'],
            "language": book['language'],
            "subjects": book['subjects'].split(','),
            "bookshelves": book['bookshelves'].split(','),
            "download_links": book['download_links'].split(',')
        }
        formatted_books.append(formatted_book)
    return formatted_books
