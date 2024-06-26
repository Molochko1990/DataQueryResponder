FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /DataQueryResponder

# Копируем требования и устанавливаем зависимости
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем все остальные файлы в контейнер
COPY . .

# Указываем команду для запуска Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
