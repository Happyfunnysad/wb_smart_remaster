import json
import os

import flet as ft

from chat_gpt import ask, ask_gpt_free
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

    def check_input(e):
        if len(url_input.value) >= 5:
            submit_btn.disabled = False
        else:
            submit_btn.disabled = True
        page.update()

    def parse(e):
        submit_btn.disabled = True
        page.update()
        feedbacks = WbReview(string=url_input.value).parse()
        if feedbacks:
            if API_KEY:
                result_gpt = ask(feedbacks=feedbacks, api_key=API_KEY)
            else:
                result_gpt = ask_gpt_free(feedbacks=feedbacks)
            change_text_in_dlg(result_gpt)
        submit_btn.disabled = False
        page.update()

    def reformat_text(text):
        text = text.replace("'", '"')
        if type(text) == str:
            text = text[text.find("{"): text.find("}") + 1]
        text = json.loads(fr"{text}")
        _plus = text.get('plus', '-')
        if _plus:
            _plus = "\n".join(_plus)
        _minus = text.get('minus', '-')
        if _minus:
            _minus = "\n".join(_minus)
        return f" Плюсы:\n{_plus}\n\n Минусы:\n{_minus}"

    def change_text_in_dlg(text):
        alert_dlg.title = ft.Text(reformat_text(text))
        page.open(alert_dlg)
        page.update()

    url_input = ft.TextField(label="Вставьте ссылку на товар или артикул", width=700, on_change=check_input)
    submit_btn = ft.FilledButton(text="Старт", width=150, disabled=True, on_click=parse)
    alert_dlg = ft.AlertDialog(title=ft.Text("ok"))

    page.add(ft.Row([url_input], alignment=ft.MainAxisAlignment.CENTER))
    page.add(ft.Row([submit_btn], alignment=ft.MainAxisAlignment.CENTER))
    page.update()


ft.app(target=main)
