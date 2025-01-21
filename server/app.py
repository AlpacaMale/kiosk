from flask import Flask, Response, request  # , jsonify 한글 인코딩 에러로 사용하지 않음
from config import Config
from models import Menu, Status, Orders, OrderItems, db
import json

# 어플리케이션 초기화
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


# 메뉴 목록 조회
@app.route("/menu", methods=["GET"])
def get_menu():
    menus = Menu.query.all()
    menus = [menu.to_dict() for menu in menus]
    print(menus)
    return Response(json.dumps(menus, ensure_ascii=False))


# 새로운 메뉴 추가
@app.route("/menu", methods=["POST"])
def add_menu():
    menu_json = request.json
    print(menu_json)
    menu_item = Menu(
        name=menu_json.get("name"),
        name_en=menu_json.get("name_en"),
        kind=menu_json.get("kind"),
        base_price=menu_json.get("base_price"),
        type=menu_json.get("type"),
        img_path=menu_json.get("img_path"),
    )
    db.session.add(menu_item)
    db.session.commit()
    # return jsonify({"message": "Menu added successfully!"}), 200
    return Response(json.dumps({"message": "Menu added successfully!"}))


# 메뉴 정보 변경
@app.route("/menu/<int:menu_id>", methods=["PUT"])
def update_menu(menu_id):
    menu_json = request.json
    print(menu_json)
    menu_item = Menu.query.filter_by(id=menu_id).first()
    menu_item.name = menu_json.get("name")
    menu_item.name_en = menu_json.get("name_en")
    menu_item.kind = menu_json.get("kind")
    menu_item.base_price = menu_json.get("base_price")
    menu_item.type = menu_json.get("type")
    menu_item.img_path = menu_json.get("img_path")
    db.session.add(menu_item)
    db.session.commit()
    # return jsonify({"message": "Menu updated successfully!"}), 200
    return Response(json.dumps({"message": "Menu updated successfully!"}))


# 메뉴 삭제
@app.route("/menu/<int:menu_id>", methods=["DELETE"])
def delete_menu(menu_id):
    menu_item = Menu.query.filter_by(id=menu_id).first()
    db.session.delete(menu_item)
    db.session.commit()
    # return jsonify({"message": "Menu deleted successfully!"}), 200
    return Response(json.dumps({"message": "Menu deleted successfully!"}))


@app.route("/order", methods=["GET"])
def get_order():
    # return jsonify()
    return Response(json.dumps({"message": "Your order"}))


@app.route("/order", methods=["POST"])
def add_order():
    # return jsonify({"message": "Order added successfully!"}), 200
    return Response(json.dumps({"message": "Order added successfully!"}))


if __name__ == "__main__":
    app.run(debug=True)
