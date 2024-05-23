import os
import sqlite3


def create_database():
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    db_path = os.path.join(parent_dir, 'knowledge_base.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subcategories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subsubcategories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subcategory_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        FOREIGN KEY (subcategory_id) REFERENCES subcategories(id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subsubcategory_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        FOREIGN KEY (subsubcategory_id) REFERENCES subsubcategories(id)
    );
    ''')

    conn.commit()
    conn.close()


create_database()
