import time
from openai import OpenAI
from g4f.client import Client


def ask(feedbacks: list, api_key):
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.proxyapi.ru/openai/v1",
    )
    content = f"На основе отзывов очень кратко напиши плюсы и минусы товара. Максимум 3 плюса и 3 минуса. " \
              f"Также укажи процентное соотношение позитивных и негативных отзывов. Пиши в формате: " \
              f"{{'plus':[здесь плюсы, процентное соотношение], 'minus':[здесь минусы, процентное соотношение]}}. " \
              f"Вот отзывы: {feedbacks}"
    
    start_time = time.time()
    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": content}]
    )
    elapsed_time = time.time() - start_time
    print(f"Анализ с использованием API ключа выполнен за {elapsed_time:.2f} секунд.")
    
    return chat_completion.choices[0].message.content


def ask_gpt_free(feedbacks: list, selected_model: str = "gpt-4o"):
    if selected_model not in AVAILABLE_MODELS:
        raise ValueError(f"Модель {selected_model} не поддерживается. Доступные модели: {AVAILABLE_MODELS}")
    
    client = Client()
    content = f"На основе отзывов кратко напиши плюсы и минусы товара. В процентном соотношении укажи количество " \
              f"позитивных и негативных отзывов (в цифрах без лишних слов). Максимум 10 плюса и 10 минуса. " \
              f"Пиши в формате: {{'plus':[здесь плюсы и процентное соотношение писать в только цифрах, в конце добавляй %], 'minus':[здесь минусы и процентное соотношение писать в только в цифрах, в конце добавляй %]}}. " \
              f"Вот отзывы: {feedbacks}"
    
    try:
        start_time = time.time()
        response = client.chat.completions.create(
            model=selected_model,
            messages=[{"role": "user", "content": content}],
        )
        elapsed_time = time.time() - start_time
        print(f"Анализ с использованием модели {selected_model} выполнен за {elapsed_time:.2f} секунд.")
        
        return response.choices[0].message.content
    except Exception as err:
        print(err)
        return None



AVAILABLE_MODELS = ["gpt-4o", "gpt-4o-mini", "claude-3.5-sonnet","gemini-pro"]
