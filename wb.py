import json

import requests
import re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}


class WbReview:
    def __init__(self, string: str):
        self.sku = self.get_sku(string=string)
        self.root_id = self.get_root_id(sku=self.sku)

    @staticmethod
    def get_sku(string: str) -> str:
        """Получение артикула"""
        if "wildberries" in string:
            pattern = r"\d{7,15}"
            sku = re.findall(pattern=pattern, string=string)
            if sku:
                return sku[0]
            else:
                raise Exception("Не удалось найти артикул")
        return string

    def get_review(self) -> json:
        """Получение отзывов"""
        try:
            response = requests.get(f'https://feedbacks1.wb.ru/feedbacks/v1/{self.root_id}', headers=HEADERS)
            if response.status_code == 200:
                if not response.json()["feedbacks"]:
                    raise Exception("Сервер 1 не подошел")
                return response.json()
        except Exception:
            response = requests.get(f'https://feedbacks2.wb.ru/feedbacks/v1/{self.root_id}', headers=HEADERS)
            if response.status_code == 200:
                return response.json()

    @staticmethod
    def get_root_id(sku: str):
        """Получение id родителя"""
        response = requests.get(
            f'https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-8144334&spp=30&nm={sku}',
            headers=HEADERS,
        )
        if response.status_code != 200:
            raise Exception("Не удалось определить id родителя")
        root_id = response.json()["data"]["products"][0]["root"]
        item_name = response.json()["data"]["products"][0]["name"]
        print(item_name)
        return root_id

    def parse(self):
        json_feedbacks = self.get_review()
        feedbacks = [feedback.get("text") for feedback in json_feedbacks["feedbacks"]
                     if str(feedback.get("nmId")) == self.sku]
        if len(feedbacks) > 80:
            feedbacks = feedbacks[:80]
        return feedbacks
