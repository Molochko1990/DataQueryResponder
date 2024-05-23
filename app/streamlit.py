import streamlit as st
import sqlite3

conn = sqlite3.connect('C:\\Users\\gaevf\\Downloads\\knowledge_base.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM articles")
rows = cursor.fetchall()

files = {}
for row in rows:
    category = row[0]  # Первая колонка - категория
    subcategory = row[1]  # Вторая колонка - подкатегория
    subcategory_data = {row[1]: row[2] for row in rows if row[0] == category and row[1] == subcategory}

    if category not in files:
        files[category] = {}

    files[category][subcategory] = subcategory_data

left1_column, right2_column = st.columns([1, 4])
inside_left, inside_right = right2_column.columns([4, 1])
# inside_right.markdown("<style>div.stButton > button:first-child { margin-top: 100px; }</style>", unsafe_allow_html=True)
st.markdown(
    """
    <style>
    #my-button {
        margin-bottom: 17px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
results = ''


def base():
    components = {}
    global results
    print(files.values())
    for categories in files.values():
        for test in list(categories.keys()):
            components[test] = st.expander(test)

            for subcategory in categories.values():
                print('xyuuuuuuuuuuuu', subcategory)
                for title in list(subcategory.keys()):
                    components[test].title(title)
                    components[test].write(subcategory[title])
                print(components.keys())

    # print('aboba', str(list(theme.values())[:]))
    # results += str(list(theme.values())[:])


def process_query(query):
    global results
    right2_column.write(f'Вы ввели запрос: {query}')
    print(files.values())
    for subcategory in files.values():
        for theme in subcategory.values():
            if query in theme:
                results = list(theme)[0]


main_page = st.container()


def create_list(data, level=0):
    global results
    for key, value in data.items():
        with st.sidebar:
            if isinstance(value, dict):
                if st.checkbox('➖' * level + str(key)):
                    create_list(value, level + 1)
            else:
                if st.checkbox('➖' * level + str(key)):
                    with main_page:
                        results = value


query = st.sidebar.text_input('', label_visibility='collapsed')
if st.sidebar.button('🔍', key="my-button"):
    process_query(query)

create_list(files)

st.write(results)

# путь к базе
# database_path = "C:\\Users\\gaevf\\PycharmProjects\\ProjectStreamlit\\wikipedia_articles.db"
