from openai import OpenAI

api_key = ''

client = OpenAI(api_key=api_key)


def fetch_gpt_response(question_and_answer=None):
    messages = [{"role": "system",
                 "content": "Согласно контексту из базы знаний дай ответ пользователя на поставленный вопрос. Не придумывай лишней информации. Использую только то, что есть в базе знаний. Ответ дай максимально кратким."},
                {"role": "user", "content": question_and_answer}]

    gpt_response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # gpt-4-turbo-preview
        messages=messages
    )

    return gpt_response


