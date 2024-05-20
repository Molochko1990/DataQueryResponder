import sqlite3


def insert_data():
    conn = sqlite3.connect('../knowledge_base.db')
    cursor = conn.cursor()

    cursor.executemany('''
    INSERT INTO categories (name) VALUES (?)
    ''', [('Общая информация о компании',), ('Административные процедуры',), ('Инструменты и программное обеспечение',), ('Рабочие процессы и стандарты',), ('Отделы и команды',), ('Обучение и развитие',), ('Вопросы и ответы',)])

    cursor.execute('SELECT id FROM categories WHERE name = ?', ('Общая информация о компании',))
    category_id = cursor.fetchone()[0]

    cursor.executemany('''
    INSERT INTO subcategories (category_id, name) VALUES (?, ?)
    ''', [(category_id, 'История компании'), (category_id, 'Миссия и ценности')])

    cursor.execute('SELECT id FROM subcategories WHERE name = ?', ('История компании',))
    subcategory_id = cursor.fetchone()[0]

    cursor.executemany('''
    INSERT INTO subsubcategories (subcategory_id, name) VALUES (?, ?)
    ''', [(subcategory_id, 'Основатели'), (subcategory_id, 'Этапы развития')])

    cursor.execute('SELECT id FROM subsubcategories WHERE name = ?', ('Основатели',))
    subsubcategory_id = cursor.fetchone()[0]

    cursor.executemany('''
    INSERT INTO articles (subsubcategory_id, title, content) VALUES (?, ?, ?)
    ''', [(subsubcategory_id, 'Основатели компании', 'Информация об основателях компании...'), (subsubcategory_id, 'Этапы развития', 'Описание этапов развития компании...')])

    conn.commit()
    conn.close()

if __name__ == '__main__':
    insert_data()
