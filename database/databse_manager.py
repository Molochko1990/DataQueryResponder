import sqlite3

def connect_to_database(database_path):
    conn = sqlite3.connect(database_path)
    return conn

def disconnect_from_database(conn):
    if conn:
        conn.close()

def fetch_data(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    data = cursor.fetchall()
    cursor.close()
    return data

def execute_query(conn, query, data=None):
    cursor = conn.cursor()
    if data:
        cursor.execute(query, data)
    else:
        cursor.execute(query)
    conn.commit()
    cursor.close()

if __name__ == "__main__":
    try:
        database_path = 'knowledge_base.db'
        conn = connect_to_database(database_path)

        tables = ['categories', 'subcategories', 'subsubcategories', 'articles']

        data = {}
        for table_name in tables:
            data[table_name] = fetch_data(conn, table_name)

        print(data)

        disconnect_from_database(conn)
    except sqlite3.OperationalError as e:
        print(e)

