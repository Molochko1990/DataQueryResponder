import sqlite3
from docx import Document


def insert_data_from_word(word_file_path):
    conn = sqlite3.connect('../knowledge_base.db')
    cursor = conn.cursor()

    try:
        doc = Document(word_file_path)
    except Exception as e:
        print(f"Error opening document: {e}")
        return
    categories = {}
    subcategories = {}
    subsubcategories = {}
    articles = []

    current_category = None
    current_subcategory = None
    current_subsubcategory = None

    for para in doc.paragraphs:
        if para.style.name == 'Heading 1':
            current_category = para.text.strip()
            cursor.execute('INSERT INTO categories (name) VALUES (?)', (current_category,))
            cursor.execute('SELECT id FROM categories WHERE name = ?', (current_category,))
            categories[current_category] = cursor.fetchone()[0]
            current_subcategory = None
            current_subsubcategory = None
        elif para.style.name == 'Heading 2':
            current_subcategory = para.text.strip()
            category_id = categories[current_category]
            cursor.execute('INSERT INTO subcategories (category_id, name) VALUES (?, ?)', (category_id, current_subcategory))
            cursor.execute('SELECT id FROM subcategories WHERE name = ?', (current_subcategory,))
            subcategories[current_subcategory] = cursor.fetchone()[0]
            current_subsubcategory = None
        elif para.style.name == 'Heading 3':
            current_subsubcategory = para.text.strip()
            subcategory_id = subcategories[current_subcategory]
            cursor.execute('INSERT INTO subsubcategories (subcategory_id, name) VALUES (?, ?)', (subcategory_id, current_subsubcategory))
            cursor.execute('SELECT id FROM subsubcategories WHERE name = ?', (current_subsubcategory,))
            subsubcategories[current_subsubcategory] = cursor.fetchone()[0]
        elif para.text.strip() and current_subsubcategory:
            subsubcategory_id = subsubcategories[current_subsubcategory]
            content = para.text.strip()
            articles.append((subsubcategory_id, content))

    # Вставляем статьи
    cursor.executemany('''
    INSERT INTO articles (subsubcategory_id, content) VALUES (?, ?)
    ''', articles)

    conn.commit()
    conn.close()


insert_data_from_word('test_db.docx')
