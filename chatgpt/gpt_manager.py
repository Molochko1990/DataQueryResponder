from openai import OpenAI

api_key = ''

client = OpenAI(api_key=api_key)


def fetch_gpt_response(question, answer):
    messages = [{"role": "system",
                 "content": f"Дай ответ на вопрос {question} согласно контексту из базы знаний. Не придумывай лишней информации. Использую только то, что есть в базе знаний. Ответ дай максимально краткий."},
                {"role": "user", "content": answer}]

    gpt_response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # gpt-4-turbo-preview
        messages=messages
    )
    print(gpt_response.choices[0].message.content)
    return gpt_response.choices[0].message.content