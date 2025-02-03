from flask import (
    Flask,
    Response,
    send_file,
    request,
    session,
    render_template,
    redirect,
)  # , jsonify 한글 인코딩 에러로 사용하지 않음
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import Menu, Users, Status, Orders, OrderItems, db
from function import login_required
import requests
import json
import os

HOST_IP = "http://127.0.0.1:5000"

# 어플리케이션 초기화
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


@app.route("/")
def _():
    return redirect("/admin")


# 메뉴 목록 조회
@app.route("/menus", methods=["GET"])
def get_menus():
    menus = Menu.query.all()
    if not menus:
        return Response(json.dumps({"message": "Menu doesn't exist!"}), status=400)
    menus = [menu.to_dict() for menu in menus]
    print(menus)
    return Response(json.dumps(menus, ensure_ascii=False), status=200)


# 특정 메뉴 목록 조회
@app.route("/menus/<int:menu_id>", methods=["GET"])
def get_menu(menu_id):
    menu = Menu.query.filter_by(id=menu_id).first()
    if not menu:
        return Response(json.dumps({"message": "Menu doesn't exist!"}), status=400)
    menu = menu.to_dict()
    print(menu)
    return Response(json.dumps(menu, ensure_ascii=False), status=200)


# 새로운 메뉴 추가
@app.route("/menus", methods=["POST"])
def add_menu():
    menu_json = request.json
    print(menu_json)
    menu_item = Menu(
        name=menu_json.get("name"),
        name_en=menu_json.get("name_en"),
        kind=menu_json.get("kind"),
        base_price=menu_json.get("base_price"),
        type=menu_json.get("type"),
        # img_path=menu_json.get("img_path"),
    )

    # DB에서 메뉴의 ID 알아내기
    db.session.add(menu_item)
    db.session.commit()

    menu_item = Menu.query.filter_by(
        name=menu_json.get("name"),
        kind=menu_json.get("kind"),
        type=menu_json.get("type"),
    ).first()

    # 알아낸 ID를 통해서 img url 설정
    img_path = f"{HOST_IP}/images/menus/{menu_item.id}"
    menu_item.img_path = img_path
    db.session.commit()

    # 설정한 img url로 이미지 파일 다운로드
    # 이미지 폴더 생성
    os.makedirs("server/images/menus", exist_ok=True)
    # 이미지 다운로드 후에 로컬 images에 저장
    response = requests.get(menu_json.get("img_path"), stream=True)
    if response.status_code == 200:
        with open(f"server/images/menus/{menu_item.id}.jpg", "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    # return jsonify({"message": "Menu added successfully!"}), 200
    return Response(json.dumps({"message": "Menu added successfully!"}), status=200)


# 메뉴 정보 변경
@app.route("/menus/<int:menu_id>", methods=["PUT"])
def update_menu(menu_id):
    menu_json = request.json
    print(menu_json)
    menu_item = Menu.query.filter_by(id=menu_id).first()
    if not menu_item:
        return Response(json.dumps({"message": "Menu doesn't exist!"}), status=400)
    menu_item.name = menu_json.get("name")
    menu_item.name_en = menu_json.get("name_en")
    menu_item.kind = menu_json.get("kind")
    menu_item.base_price = menu_json.get("base_price")
    menu_item.type = menu_json.get("type")
    menu_item.img_path = menu_json.get("img_path")
    db.session.add(menu_item)
    db.session.commit()
    # return jsonify({"message": "Menu updated successfully!"}), 200
    return Response(json.dumps({"message": "Menu updated successfully!"}), status=200)


# 메뉴 삭제
@app.route("/menus/<int:menu_id>", methods=["DELETE"])
def delete_menu(menu_id):
    menu_item = Menu.query.filter_by(id=menu_id).first()
    if not menu_item:
        return Response(json.dumps({"message": "Menu doesn't exist!"}), status=400)
    db.session.delete(menu_item)
    db.session.commit()
    # return jsonify({"message": "Menu deleted successfully!"}), 200
    return Response(json.dumps({"message": "Menu deleted successfully!"}), status=200)


# 메뉴 이미지 전송
@app.route("/images/menus/<int:menu_id>", methods=["GET"])
def get_menu_img(menu_id):
    # 쿼리 파라미터 확인
    # data = request.args
    # print(json.dumps(data))
    img_path = f"images/menus/{menu_id}.jpg"
    return send_file(img_path, mimetype="image/jpeg")


# 프로필 이미지 전송
@app.route("/images/profile/<int:user_id>", methods=["GET"])
def get_profile_img(user_id):
    profile_img = f"images/profile/{user_id}.jpg"
    return send_file(profile_img, mimetype="image/jpeg")


@app.route("/orders", methods=["GET"])
def get_orders():
    # return jsonify()
    return Response(json.dumps({"message": "Your order"}))


@app.route("/orders", methods=["POST"])
def add_order():
    # return jsonify({"message": "Order added successfully!"}), 200
    return Response(json.dumps({"message": "Order added successfully!"}))


# 특정 유저 조회
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    # 현재 로그인 되어있는 유저가 관리자거나,
    # 조회하려고 하는 유저와 일치한다면 조회하기
    logged_in_user = Users.query.filter_by(email=session.get("email")).first()
    if not logged_in_user:
        return Response(json.dumps({"message": "You must logged in!"}), status=400)
    if not (user_id == logged_in_user.id or logged_in_user.role == "admin"):
        return Response(
            json.dumps({"message": "You don't have authorize!"}), status=401
        )

    user = Users.query.filter_by(id=user_id).first()
    if not user:
        return Response(json.dumps({"message": "User doesn't exist!"}), status=400)
    user = user.to_dict()
    print(user)
    return Response(json.dumps(user, ensure_ascii=False), status=200)


# 새로운 유저 추가
@app.route("/users", methods=["POST"])
def add_user():
    session.pop("email", None)
    user_json = request.json
    print(user_json)

    # email이 이미 있는지 찾기
    user = Users.query.filter_by(email=user_json.get("email")).first()
    if user:
        return Response(json.dumps({"message": "User aleady exist!"}), status=400)

    user = Users(
        email=user_json.get("email"),
        password=generate_password_hash(user_json.get("password")),
        role=user_json.get("role"),
        profile_image=user_json.get("profile_image"),
    )
    db.session.add(user)
    db.session.commit()
    return Response(json.dumps({"message": "User added successfully!"}), status=200)


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    # 현재 로그인 되어있는 유저가 관리자거나,
    # 삭제하려고 하는 유저와 일치한다면 조회하기
    logged_in_user = Users.query.filter_by(email=session.get("email")).first()
    if not logged_in_user:
        return Response(json.dumps({"message": "You must logged in!"}), status=400)
    if not (user_id == logged_in_user.id or logged_in_user.role == "admin"):
        return Response(
            json.dumps({"message": "You don't have authorize!"}), status=401
        )

    user = Users.query.filter_by(id=user_id).first()
    if not user:
        return Response(json.dumps({"message": "User doesn't exist!"}), status=400)
    db.session.delete(user)
    db.session.commit()
    return Response(json.dumps({"message": "User deleted successfully!"}), status=200)


# 로그인 api
@app.route("/api/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")
    user = Users.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return Response(json.dumps({"message": "Login Failed!"}), status=400)
    session["email"] = email
    print(f"Logged in", session.get("email"))
    return Response(json.dumps({"message": "Login success!"}), status=200)


# 로그아웃 api
@app.route("/api/logout", methods=["POST"])
def logout():
    session.pop("email", None)
    return Response(json.dumps({"message": "Logout success!"}), status=200)


# 관리자 회원가입 페이지
@app.route("/admin/register", methods=["GET", "POST"])
def admin_register():
    if request.method == "POST":
        pass
    else:
        return render_template("register.html")


# 관리자 로그인 페이지
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        pass
    else:
        return render_template("login.html")


# 관리자 페이지
@app.route("/admin", methods=["GET"])
@login_required
def admin():
    # todo db
    return render_template("index.html", user=session.get("email"))


if __name__ == "__main__":
    app.run(debug=True)
