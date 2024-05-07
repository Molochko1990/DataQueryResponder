from search import semantic_search as ss

import streamlit as st

st.title('Умный ассистент')
query = st.text_input('Введите ваш запрос:')
def process_query(query):
    st.write(f'Вы ввели запрос: {query}')
    st.write(ss.SemanticSearch(query))

if st.button('Отправить запрос'):
    process_query(query)