import json
import os

import flet as ft

from chat_gpt import ask, ask_gpt_free, AVAILABLE_MODELS
from wb import WbReview
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')
API_KEY = os.getenv("CHAT_GPT_API_KEY")


def main(page: ft.Page):
    page.title = "WB Smart Review"
    page.theme_mode = "dark"
    page.window.width = 900
    page.window.height = 600
    page.window.resizable = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    if not API_KEY:
        print("Нет api ключа")

    model_dropdown = ft.Dropdown(
        label="Выберите модель",
        width=200,
        options=[ft.dropdown.Option(model) for model in AVAILABLE_MODELS],
        value=AVAILABLE_MODELS[0]  # По умолчанию выбираем первую модель
    )

    def check_input(e):
        if len(url_input.value) >= 5:
            submit_btn.disabled = False
        else:
            submit_btn.disabled = True
        page.update()

    def parse(e):
        print("Начинаю процесс парсинга и анализа отзывов...")
        submit_btn.disabled = True
        page.update()
        feedbacks = WbReview(string=url_input.value).parse()
        if feedbacks:
            try:
                if API_KEY:
                    print("Отправляю отзывы на анализ с использованием API ключа...")
                    result_gpt = ask(feedbacks=feedbacks, api_key=API_KEY)
                else:
                    print("Отправляю отзывы на бесплатный анализ...")
                    result_gpt = ask_gpt_free(feedbacks=feedbacks, selected_model=model_dropdown.value)
                change_text_in_dlg(result_gpt)
            except Exception as err:
                print(f"Ошибка при анализе: {err}")
                show_retry_button()
        submit_btn.disabled = False
        page.update()

    def show_retry_button():
        retry_btn = ft.FilledButton(text="Повторить запрос", on_click=parse)
        page.add(ft.Row([retry_btn], alignment=ft.MainAxisAlignment.CENTER))
        page.update()

    def reformat_text(text):
        try:
            text = text.replace("'", '"')
            if type(text) == str:
                text = text[text.find("{"): text.find("}") + 1]
            text = json.loads(fr"{text}")
            _plus = text.get('plus', '-')
            if _plus:
                _plus_text = "\n".join(_plus[:-1])  # Извлекаем текст плюсов
                _plus_percentage = _plus[-1]  # Извлекаем процентное соотношение
            _minus = text.get('minus', '-')
            if _minus:
                _minus_text = "\n".join(_minus[:-1])  # Извлекаем текст минусов
                _minus_percentage = _minus[-1]  # Извлекаем процентное соотношение
            return f" Плюсы:\n{_plus_text}\nПроцент положительных отзывов: {_plus_percentage}\n\n Минусы:\n{_minus_text}\nПроцент отрицательных отзывов: {_minus_percentage}"
        except json.JSONDecodeError as e:
            print(f"Ошибка декодирования JSON: {e}")
            return "Ошибка анализа данных. Пожалуйста, попробуйте снова."

    def change_text_in_dlg(text):
        alert_dlg.content.content.controls[0].value = reformat_text(text)
        page.open(alert_dlg)
        page.update()

    def new_request(e):
        url_input.value = ""
        submit_btn.disabled = True
        alert_dlg.open = False
        page.update()

    url_input = ft.TextField(
        label="Вставьте ссылку на товар или артикул",
        expand=True,  # Позволяет текстовому полю расширяться
        on_change=check_input
    )
    submit_btn = ft.FilledButton(
        text="Старт",
        width=150,
        disabled=True,
        on_click=parse
    )
    alert_dlg = ft.AlertDialog(
        title=ft.Text("Результаты анализа"),
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "",  # Пустая строка, будет обновляться позже
                        expand=True,
                        max_lines=None  # Позволяет тексту занимать больше строк
                    )
                ],
                scroll=ft.ScrollMode.AUTO  # Добавляем прокрутку
            ),
            width=page.window.width * 0.8,
            height=page.window.height * 0.5,
            padding=10,  # Используем числовое значение для отступов
            expand=True
        ),
        # Добавляем кнопку "Новый запрос"
        actions=[
            ft.FilledButton("Новый запрос", on_click=new_request)
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    page.add(
        ft.Row(
            [url_input], 
            alignment=ft.MainAxisAlignment.CENTER, 
            expand=True
        )
    )
    page.add(
        ft.Row(
            [model_dropdown, submit_btn], 
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
    page.update()


ft.app(target=main)
