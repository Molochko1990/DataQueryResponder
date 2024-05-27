import streamlit as st
import sqlite3
from database import semantic_search as ss
#
#
#
#conn = sqlite3.connect('database/knowledge_base.db')
#
#cursorart = conn.cursor()
#
#cursorart.execute("SELECT * FROM articles")
#
#rows = cursorart.fetchall()
#
#files = {}
#
left1_column, right2_column = st.columns([1, 4])
inside_left, inside_right = right2_column.columns([4, 1])
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

ResultsList = []
ResultsListSub = []
def process_query(query):
    global results
    right2_column.write(f'Вы ввели запрос: {query}')
    nglobal_results = ss.elastic_output(query)
    for result in nglobal_results:
        ResultsList.append(result['articles'])
        ResultsListSub.append([result['subcategory'], result['subsubcategory']])

#История компании

#Расскажи историю компании

#main_page = st.container()





#def create_list(data, level=0):
#    global results
#    for key, value in data.items():
#        with st.sidebar:
#            if isinstance(value, dict):
#                if st.checkbox('➖' * level + str(key)):
#                    create_list(value, level + 1)
#            else:
#                if st.checkbox('➖' * level + str(key)):
#                    with main_page:
#                        results = value






# путь к базе
# database_path = "C:\\Users\\gaevf\\PycharmProjects\\ProjectStreamlit\\wikipedia_articles.db"

# Функция для сохранения состояния сессии
def save_session_state(selected_category, selected_subcategory, selected_content):
    session_state = {
        'selected_category': selected_category,
        'selected_subcategory': selected_subcategory,
        'selected_content': selected_content
    }
    return session_state

# Функция для восстановления состояния сессии
def restore_session_state():
    session_state = st.session_state.get('session_state', None)
    if session_state:
        return session_state['selected_category'], session_state['selected_subcategory'], session_state['selected_content']
    else:
        return None, None, None

# Функция для чтения базы данных
def read_database():
    conn = sqlite3.connect('database/knowledge_base.db')
    cursor = conn.cursor()

    cursor.execute("SELECT categories.name, subcategories.name, subsubcategories.name, articles.content "
                   "FROM categories "
                   "JOIN subcategories ON categories.id = subcategories.category_id "
                   "JOIN subsubcategories ON subcategories.id = subsubcategories.subcategory_id "
                   "JOIN articles ON subsubcategories.id = articles.subsubcategory_id")

    rows = cursor.fetchall()

    hierarchy = {}
    for row in rows:
        category = row[0]
        subcategory = row[1]
        subsubcategory = row[2]
        content = row[3]

        if category not in hierarchy:
            hierarchy[category] = {}

        if subcategory not in hierarchy[category]:
            hierarchy[category][subcategory] = []

        if content not in hierarchy[category][subcategory]:
            hierarchy[category][subcategory].append(content)

    return hierarchy

# Восстановление состояния сессии
selected_category, selected_subcategory, selected_content = restore_session_state()

# Чтение базы данных
hierarchy = read_database()

st.sidebar.title('Категории')

query = st.sidebar.text_input('', label_visibility='collapsed')
if st.sidebar.button('🔍', key="my-button"):
    process_query(query)
    for i in range(len(ResultsList)):
       expName = ResultsListSub[i][0] + ' - ' + ResultsListSub[i][1]
       currentEsp = st.expander(expName, expanded=True)
       with currentEsp:
           st.write(ResultsList[i])
    st.write("------------------")
    st.write('Информация из выбранных категорий: ', )


# Выбор категории
selected_category = st.sidebar.selectbox('Выберите категорию', list(hierarchy.keys()), index=list(hierarchy.keys()).index(selected_category) if selected_category else 0)

if selected_category in hierarchy and hierarchy[selected_category]:
    subcategories = list(hierarchy[selected_category].keys())
    selected_subcategory = st.sidebar.selectbox('Выберите подкатегорию', subcategories, index=subcategories.index(selected_subcategory) if selected_subcategory in subcategories else 0)

if selected_subcategory:
    for content in hierarchy[selected_category][selected_subcategory]:
        expName = selected_category + ' - ' + selected_subcategory
        currentEsp = st.expander(expName, expanded=True)
        with currentEsp:
            st.write(content)

# Сохранение состояния сессии
session_state = save_session_state(selected_category, selected_subcategory, selected_content)
st.session_state['session_state'] = session_state