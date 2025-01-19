import requests
import json

url = "http://127.0.0.1:5000/menu"
headers = {"Content-Type": "application/json; charset=utf-8"}


def get_menu():
    response = requests.get(url, headers=headers)
    print(response.text)


def post_menu():
    data = {
        "name": "아메리카노",
        "name_en": "americano",
        "kind": "coffee",
        "price": 3000,
        "type": ["ice", "hot"],
        "size": ["tall", "grande", "venti"],
        "ice": ["no", "half", "regular"],
        "img_path": "./img/americano",
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)


def update_menu():
    data = {
        "name": "에스프레소",
        "name_en": "espresso",
        "kind": "coffee",
        "price": 3000,
        "img_path": "./img/espresso",
    }
    response = requests.put(f"{url}/1", headers=headers, data=json.dumps(data))
    print(response.text)


def delete_menu():
    response = requests.delete(f"{url}/2", headers=headers)
    print(response.text)


post_menu()
