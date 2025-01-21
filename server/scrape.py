from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
from config import url


# 찾아낼것 =

p = sync_playwright().start()
browser = p.chromium.launch(headless=False)
page = browser.new_page()
page.goto(url)
time.sleep(2)
menus = []


def collect_menu_info(number, kind):
    page.click(f"input[value='{number}']", force=True)
    time.sleep(1)
    content = page.content()
    page.click(f"input[value='{number}']", force=True)
    soup = BeautifulSoup(content, "html.parser")
    menu_list = soup.select("#menu_list > li")

    for menu in menu_list:
        modal = menu.find("div", class_="inner_modal")
        menu_data = {
            "img_url": menu.find("img")["src"],
            "type": menu.find("div", class_="cont_gallery_list_label").text.lower(),
            "name": modal.find("div", class_="cont_text_title").text.strip(),
            "name_en": modal.find("div", class_="cont_text_info").text.strip(),
            "kind": kind,
        }
        menus.append(menu_data)


collect_menu_info(1, "coffee")
collect_menu_info(2, "tee")
collect_menu_info(4, "smoothie")
collect_menu_info(5, "decaffeine")
collect_menu_info(6, "beverage")

with open("server/coffee.csv", "w", encoding="utf-8") as file:
    file.write("name,name_en,kind,type,img_path\n")
    for menu in menus:
        file.write(
            f"{menu["name"]},{menu["name_en"]},{menu["kind"]},{menu["type"]},{menu["img_url"]}\n"
        )
