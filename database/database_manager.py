import sqlite3


class DBManager:
    def __init__(self, sqlite_db_path='database/knowledge_base.db'):
        self.sqlite_db_path = sqlite_db_path
        self.sqlite_conn = sqlite3.connect(self.sqlite_db_path)
        self.cursor = self.sqlite_conn.cursor()

    def fetch_data(self, batch_size=1000):
        self.cursor.execute('''
            SELECT a.id, a.content, s.name AS subsubcategory, sc.name AS subcategory, c.name AS category
            FROM articles a
            JOIN subsubcategories s ON a.subsubcategory_id = s.id
            JOIN subcategories sc ON s.subcategory_id = sc.id
            JOIN categories c ON sc.category_id = c.id
        ''')

        while True:
            rows = self.cursor.fetchmany(batch_size)
            if not rows:
                break
            yield rows

    def close_connection(self):
        self.sqlite_conn.close()
