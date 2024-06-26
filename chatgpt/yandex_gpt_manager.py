import requests
url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Api-Key #your api"
}
def fetch_yandex_gpt_response(question = None, answer = None):
    prompt = {
        "modelUri": "gpt://b1gks3qh14qma0kud95t/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "10000"
        },
        "messages": [
            {
                "role": "system",
                "text": f"Дай ответ на вопрос {question} согласно контексту из базы знаний. Не придумывай лишней информации. Использую только то, что есть в базе знаний. Ответ дай максимально краткий."
            },
            {
                "role": "user",
                "text": answer
            },
        ]
    }
    response = requests.post(url, headers=headers, json=prompt)
    answer = response.json()
    answer = answer['result']['alternatives'][0]['message']['text']

    return (answer)
