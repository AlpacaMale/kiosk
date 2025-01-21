import requests
import json
from enum import Enum
import random

url = "http://127.0.0.1:5000/menu"
headers = {"Content-Type": "application/json; charset=utf-8"}


def get_menu():
    response = requests.get(url, headers=headers)
    print(response.text)


def post_menu(name, name_en, kind, base_price, type, img_path):
    data = {
        "name": name,
        "name_en": name_en,
        "kind": kind,
        "base_price": base_price,
        "type": type,
        "img_path": img_path,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)


def update_menu():
    data = {
        "name": "에스프레소",
        "name_en": "espresso",
        "kind": "coffee",
        "base_price": 3000,
        "img_path": "./img/espresso",
    }
    response = requests.put(f"{url}/1", headers=headers, data=json.dumps(data))
    print(response.text)


def delete_menu():
    response = requests.delete(f"{url}/2", headers=headers)
    print(response.text)


with open("server/coffee.csv", "r", encoding="utf-8") as file:
    for line in file:
        name, name_en, kind, type, img_path = line.split(",")
        img_path = img_path.strip()
        base_price = random.choice([3000, 4000, 4500, 5500])
        # print(base_price)
        post_menu(name, name_en, kind, base_price, type, img_path)
