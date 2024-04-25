from openai import OpenAI

api_key = ''

client = OpenAI(api_key=api_key)


def fetch_gpt_response(question_and_answer=None):
  messages = [{"role": "system",
               "content": "Ты должен опираясь на ответ из базы знаний ( данные хранятся в формате вопрос ; ответ) дать логичный ответ на поставленный вопрос пользователя. Не придумывай лишней информации. Использую только то, что есть в базе знаний. Можно переформулировать ответ."},
              {"role": "user", "content": question_and_answer}]

  gpt_response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # gpt-4-turbo-preview
    messages=messages
  )
  # Вывод ответа модели
  return gpt_response
s=str(input())
print(fetch_gpt_response(s))