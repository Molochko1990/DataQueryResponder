import streamlit as st
from PIL import Image

# Добавление вкладок
tabs = ["Главная", "Краткое описание", "Доп. Информация"]
selected_tab = st.sidebar.radio("Выберите вкладку", tabs)

# Заголовок приложения
st.title('Умный ассистент')

# Поле для ввода запроса
query = st.text_input('Введите ваш запрос:')


# Функция для обработки запроса и вывода данных
def process_query(query):
    # Здесь можно добавить логику обработки запроса и получения данных
    # Например, можно использовать pandas для работы с данными

    # Пример вывода данных
    st.write(f'Вы ввели запрос: {query}')
    st.write('Здесь могут быть данные, соответствующие вашему запросу')


# Обработка запроса при нажатии кнопки
if st.button('Отправить запрос'):
    process_query(query)

# Отображение информации в зависимости от выбранной вкладки
if query == "":
    if selected_tab == "Главная":
        subtabs = ["1.1", "1.2", "1.3"]
        selected_subtab = st.sidebar.radio("Подвкладка", subtabs)
        if selected_subtab == "1.1":
            st.write("Содержимое подвкладки 1.1")
        elif selected_subtab == "1.2":
            st.write("Содержимое подвкладки 1.2")
        elif selected_subtab == "1.3":
            st.write("Содержимое подвкладки 1.3")
    elif selected_tab == "Краткое описание":
        subtabs = ["2.1", "2.2", "2.3"]
        selected_subtab = st.sidebar.radio("Подвкладка", subtabs)
        if selected_subtab == "2.1":
            st.write("Содержимое подвкладки 2.1")
        elif selected_subtab == "2.2":
            st.write("Содержимое подвкладки 2.2")
        elif selected_subtab == "2.3":
            st.write("Содержимое подвкладки 2.3")
    elif selected_tab == "Доп. Информация":
        subtabs = ["3.1", "3.2", "3.3"]
        selected_subtab = st.sidebar.radio("Подвкладка", subtabs)
        if selected_subtab == "3.1":
            st.write("Содержимое подвкладки 3.1")
        elif selected_subtab == "3.2":
            st.write("Содержимое подвкладки 3.2")
        elif selected_subtab == "3.3":
            st.write("Содержимое подвкладки 3.3")
