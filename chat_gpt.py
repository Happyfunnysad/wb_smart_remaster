from openai import OpenAI
from g4f.client import Client


def ask(feedbacks: list, api_key):
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.proxyapi.ru/openai/v1",
    )
    content = f"На основе отзывов очень кратко напиши плюсы и минусы товара. Максимум 3 плюса и 3 минуса. Пиши в формате" \
              ": {'plus':[здесь плюсы], 'minus':[здесь минусы]}. Вот отзывы" + f"{feedbacks}"
    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": content}]
    )
    return chat_completion.choices[0].message.content


def ask_gpt_free(feedbacks: list):
    client = Client()
    content = f"На основе отзывов очень кратко напиши плюсы и минусы товара. Максимум 3 плюса и 3 минуса. Пиши в формате" \
              ": {'plus':[здесь плюсы], 'minus':[здесь минусы]}. Вот отзывы" + f"{feedbacks}"
    model_list = ["gpt-4-turbo", "gpt-4o-mini", "gpt-3.5-turbo"]
    for model in model_list:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": content}],
            )
            return response.choices[0].message.content
        except Exception as err:
            print(err)
            continue

