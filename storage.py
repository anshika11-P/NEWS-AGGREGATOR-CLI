import sqlite3
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

DB_FILE = BASE_DIR / "news.db"
JSON_FILE = BASE_DIR / "news.json"


def initialize_database():

    with sqlite3.connect(DB_FILE) as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                link TEXT NOT NULL UNIQUE,
                description TEXT,
                source TEXT,
                published TEXT
            )
        """)


def save_news(news):

    initialize_database()

    saved_count = 0

    with sqlite3.connect(DB_FILE) as connection:

        for item in news:

            cursor = connection.execute("""
                INSERT OR IGNORE INTO news
                (title, link, description, source, published)
                VALUES (?, ?, ?, ?, ?)
            """, (
                item["title"],
                item["link"],
                item["description"],
                item["source"],
                item["published"]
            ))

            saved_count += cursor.rowcount

    all_news = load_news()

    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(all_news, file, indent=4, ensure_ascii=False)

    return saved_count


def load_news():

    initialize_database()

    with sqlite3.connect(DB_FILE) as connection:

        connection.row_factory = sqlite3.Row

        rows = connection.execute("""
            SELECT title, link, description, source, published
            FROM news
            ORDER BY id DESC
        """).fetchall()

    return [dict(row) for row in rows]