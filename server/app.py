from flask import (
    Flask,
    Response,
    send_file,
    request,
    session,
    render_template,
    redirect,
    flash,
)  # , jsonify 한글 인코딩 에러로 사용하지 않음
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config, headers
from models import Menu, Users, Status, Orders, OrderItems, db
from function import login_required
import requests
import json
import os
import csv

HOST_IP = "http://127.0.0.1:5000"


# 어플리케이션 초기화
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
Session(app)


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
    # print(menus)
    return Response(json.dumps(menus, ensure_ascii=False), status=200)


# 특정 메뉴 목록 조회
@app.route("/menus/<int:menu_id>", methods=["GET"])
def get_menu(menu_id):
    menu = Menu.query.filter_by(id=menu_id).first()
    if not menu:
        return Response(json.dumps({"message": "Menu doesn't exist!"}), status=400)
    menu = menu.to_dict()
    # print(menu)
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
    if menu_json.get("img_path"):
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
    if menu_json.get("img_path"):
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

    # password와 pqssword-confirm이 일치하는지 찾기
    if not user_json.get("password") == user_json.get("password-confirm"):
        return Response(
            json.dumps({"message": "Password confirm does not match!"}), status=400
        )

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
    return Response(json.dumps({"message": "Login success!"}), status=200)


# 로그아웃 api
@app.route("/api/logout", methods=["POST"])
def logout():
    return Response(json.dumps({"message": "Logout success!"}), status=200)


# 관리자 회원가입 페이지
@app.route("/admin/register", methods=["GET", "POST"])
def admin_register():
    if request.method == "POST":
        data = request.form.to_dict()
        data["role"] = "admin"
        data["profile_image"] = ""

        response = requests.post(
            f"{HOST_IP}/users", headers=headers, data=json.dumps(data)
        )
        if response.status_code == 400:
            flash(response.json().get("message"))
            return redirect("/admin/register")
        else:
            return redirect("/admin")
    else:
        return render_template("register.html")


# 관리자 로그인 페이지
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        data = request.form.to_dict()
        response = requests.post(
            f"{HOST_IP}/api/login", headers=headers, data=json.dumps(data)
        )
        if response.status_code == 400:
            flash(response.json().get("message"))
            return redirect("/admin/login")
        else:
            session["email"] = data.get("email")
            return redirect("/admin")
    else:
        return render_template("login.html")


# 관리자 로그아웃 페이지
@app.route("/admin/logout", methods=["GET"])
def admin_logout():
    response = requests.post(f"{HOST_IP}/api/logout", headers=headers)
    if response.status_code == 200:
        session.pop("email", None)
    return redirect("/admin")


# 관리자 페이지
@app.route("/admin", methods=["GET"])
@login_required
def admin():
    response = requests.get(f"{HOST_IP}/menus", headers=headers)
    datas = response.json()
    return render_template("index.html", email=session.get("email"), datas=datas)


# 관리자 페이지에서 개별 메뉴 조회
@app.route("/admin/menus/<int:menu_id>", methods=["GET"])
@login_required
def admin_get_menu(menu_id):
    response = requests.get(f"{HOST_IP}/menus/{menu_id}", headers=headers)
    if response.status_code == 400:
        flash(response.text)
    data = response.json()
    response = requests.get(f"{HOST_IP}/menus", headers=headers)
    if response.status_code == 400:
        flash(response.text)
    datas = response.json()
    return render_template("menu.html", data=data, email=session.get("email"))


# 관리자 페이지에서 전체 메뉴 다운로드
# @app.route("/admin/menus", methods=["GET"])
# @login_required
# def admin_export_menu():
#     response = requests.get(f"{HOST_IP}/menus", headers=headers)
#     if response.status_code == 400:
#         flash(response.text)
#     datas = response.json()
#     os.makedirs("server/data", exist_ok=True)
#     with open("server/data/menus.csv", "w", encoding="utf-8") as file:
#         fieldnames = ["id", "name", "name_en", "kind", "base_price", "type", "img_path"]
#         writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction="ignore")
#         writer.writeheader()
#         writer.writerows(datas)
#     return send_file("data/menus.csv", mimetype="text/csv")


# 관리자 페이지에서 메뉴 추가
@app.route("/admin/menus/add", methods=["GET", "POST"])
@login_required
def admin_add_menu():
    if request.method == "POST":
        data = request.form.to_dict()
        response = requests.post(
            f"{HOST_IP}/menus", headers=headers, data=json.dumps(data)
        )
        if response.status_code == 400:
            flash(response.text)
        return redirect("/admin")
    else:
        return render_template("/add_menu.html", email=session.get("email"))


# 관리자 페이지에서 메뉴 수정
@app.route("/admin/menus/<int:menu_id>", methods=["POST"])
@login_required
def admin_update_menu(menu_id):
    data = request.form.to_dict()
    response = requests.put(
        f"{HOST_IP}/menus/{menu_id}", headers=headers, data=json.dumps(data)
    )
    if response.status_code == 400:
        flash(response.text)
    return redirect("/admin")


# 관리자 페이지에서 메뉴 삭제
@app.route("/admin/menus/<int:menu_id>/delete", methods=["GET"])
@login_required
def admin_delete_menu(menu_id):
    response = requests.delete(f"{HOST_IP}/menus/{menu_id}", headers=headers)
    if response.status_code == 400:
        flash(response.text)
    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)
