import requests
import json
from enum import Enum
import random

url = "http://127.0.0.1:5000"
headers = {"Content-Type": "application/json; charset=utf-8"}


def get_menu():
    response = requests.get(f"{url}/menu", headers=headers)
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
    response = requests.post(f"{url}/menu", headers=headers, data=json.dumps(data))
    print(response.text)


def update_menu():
    data = {
        "name": "에스프레소",
        "name_en": "espresso",
        "kind": "coffee",
        "base_price": 3000,
        "img_path": "./img/espresso",
    }
    response = requests.put(f"{url}/menu/1", headers=headers, data=json.dumps(data))
    print(response.text)


def delete_menu():
    response = requests.delete(f"{url}/menu/2", headers=headers)
    print(response.text)


def get_img():
    response = requests.get(f"{url}/img/1?width=300&height=200", headers=headers)
    print(response.text)


# get_img()


with open("server/coffee.csv", "r", encoding="utf-8") as file:
    for line in file:
        name, name_en, kind, type, img_path = line.split(",")
        if name == "name":
            continue
        img_path = img_path.strip()
        base_price = random.choice([3000, 4000, 4500, 5500])
        # print(base_price)
        post_menu(name, name_en, kind, base_price, type, img_path)
