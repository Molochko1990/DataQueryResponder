import streamlit as st
import sqlite3

left1_column, right2_column = st.columns([1, 4])
inside_left, inside_right = right2_column.columns([4, 1])
query = inside_left.text_input('', label_visibility='collapsed')
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

# Добавление вкладок
# tabs = ["Главная", "Краткое описание", "Доп. Информация"]
# selected_tab = st.sidebar.radio("Выберите вкладку", tabs)


# Функция для обработки запроса и вывода данных
def process_query(query):
    # Здесь можно добавить логику обработки запроса и получения данных
    # Например, можно использовать pandas для работы с данными

    # Пример вывода данных
    right2_column.write(f'Вы ввели запрос: {query}')
    st.write('Здесь могут быть данные, соответствующие вашему запросу')


# Обработка запроса при нажатии кнопки
if inside_right.button('🔍', key="my-button"):
    process_query(query)

# Определение структуры иерархии страниц и категорий
pages = {
    "Категория 1": ["Страница 1", "Страница 2"],
    "Категория 2": ["Страница 3", "Страница 4", "Страница 5"],
    "Категория 3": ["Страница 6"]
}

# Отображение названий страниц в боковой панели
for category, subpages in pages.items():
    st.sidebar.subheader(category)
    for subpage in subpages:
        if st.sidebar.button(subpage):
            st.write(f"Отображается страница: {subpage}")
# путь к базе
# database_path = "C:\\Users\\gaevf\\PycharmProjects\\ProjectStreamlit\\wikipedia_articles.db"
