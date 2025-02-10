from flask import (
    Flask,
    Response,
    send_file,
    request,
    session,
    render_template,
    redirect,
    flash,
    url_for,
)  # , jsonify 한글 인코딩 에러로 사용하지 않음
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import Menu, Users, db
from function import login_required
import requests
import json
import os
import csv

HOST_IP = "http://127.0.0.1:5000"

# 어플리케이션 초기화
app = Flask(__name__)

# 객체를 이용한 초기화
app.config.from_object(Config)

# db 초기화
db.init_app(app)

# 세션 초기화
Session(app)

# 디렉토리 생성
os.makedirs("server/images/menus", exist_ok=True)
os.makedirs("server/images/profile", exist_ok=True)
os.makedirs("server/datas", exist_ok=True)


# 어드민 페이지로 리디렉트
@app.route("/")
def _():
    return redirect(url_for("home"))


# 메뉴 목록 조회 api
@app.route("/menus", methods=["GET"])
def get_menus():
    menus = Menu.query.all()
    if not menus:
        return Response(json.dumps({"message": "Menu doesn't exist!"}), status=400)
    menus = [menu.to_dict() for menu in menus]
    return Response(json.dumps(menus, ensure_ascii=False), status=200)


# 특정 메뉴 목록 조회 api
@app.route("/menus/<int:menu_id>", methods=["GET"])
def get_menu(menu_id):
    menu = Menu.query.filter_by(id=menu_id).first()
    if not menu:
        return Response(json.dumps({"message": "Menu doesn't exist!"}), status=400)
    menu = menu.to_dict()
    return Response(json.dumps(menu, ensure_ascii=False), status=200)


# 새로운 메뉴 추가 api
# 일단 db에 먼저 메뉴를 등록하고 id를 알아냅니다.
# 메뉴의 이미지 이름을 메뉴의 id와 동일하게 합니다.
@app.route("/menus", methods=["POST"])
def add_menu():

    # post로 받은 데이터를 menu로 등록합니다.
    menu_json = request.get_json(silent=True)
    if not menu_json:
        menu_json = request.form.to_dict()
    menu_item = Menu(
        name=menu_json.get("name"),
        name_en=menu_json.get("name_en"),
        kind=menu_json.get("kind"),
        base_price=menu_json.get("base_price"),
        type=menu_json.get("type"),
    )
    db.session.add(menu_item)
    db.session.commit()

    # 방금 등록한 메뉴의 id를 찾습니다.
    menu_item = Menu.query.filter_by(
        name=menu_json.get("name"),
        kind=menu_json.get("kind"),
        type=menu_json.get("type"),
    ).first()

    # 만약 데이터에 이미지 경로가 있다면 다운로드 받은 후 경로를 업데이트 해줍니다.
    if menu_json.get("img_path"):
        response = requests.get(menu_json.get("img_path"), stream=True)
        if response.status_code == 200:
            with open(f"server/images/menus/{menu_item.id}.jpg", "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

    # 만약 데이터에 파일이 있다면 파일 이름을 변경 후 저장합니다.
    elif "file" in request.files:
        file = request.files["file"]
        if file.filename != "" and allowed_file(file.filename):
            file.save(f"server/images/menus/{menu_item.id}.jpg")

    else:
        return Response(
            json.dumps({"message": "Need menu image or image url!"}), status=400
        )

    img_path = f"{HOST_IP}/images/menus/{menu_item.id}"
    menu_item.img_path = img_path
    db.session.commit()

    return Response(json.dumps({"message": "Menu added successfully!"}), status=200)


# 메뉴 정보 변경 api
@app.route("/menus/<int:menu_id>", methods=["PUT"])
def update_menu(menu_id):

    # put으로 받은 데이터를 menu로 등록합니다.
    menu_json = request.get_json(silent=True)
    if not menu_json:
        menu_json = request.form.to_dict()
    menu_item = Menu.query.filter_by(id=menu_id).first()

    # 만약 그런 메뉴가 없다면 에러 메시지를 보냅니다.
    if not menu_item:
        return Response(json.dumps({"message": "Menu doesn't exist!"}), status=400)

    # 메뉴틀 업데이트 해줍니다.
    menu_item.name = menu_json.get("name")
    menu_item.name_en = menu_json.get("name_en")
    menu_item.kind = menu_json.get("kind")
    menu_item.base_price = menu_json.get("base_price")
    menu_item.type = menu_json.get("type")

    # 만약 데이터에 파일이 있다면 파일 이름을 변경 후 저장합니다.
    if "file" in request.files:
        file = request.files["file"]
        if file.filename != "" and allowed_file(file.filename):
            file.save(f"server/images/menus/{menu_item.id}.jpg")

    # db에 저장해줍니다.
    db.session.add(menu_item)
    db.session.commit()

    return Response(json.dumps({"message": "Menu updated successfully!"}), status=200)


# 메뉴 삭제 api
@app.route("/menus/<int:menu_id>", methods=["DELETE"])
def delete_menu(menu_id):

    # menu_id를 이용해서 메뉴를 찾습니다.
    menu_item = Menu.query.filter_by(id=menu_id).first()

    # menu가 없다면 에러를 출력합니다.
    if not menu_item:
        return Response(json.dumps({"message": "Menu doesn't exist!"}), status=400)

    # 메뉴를 삭제합니다.
    db.session.delete(menu_item)
    db.session.commit()

    return Response(json.dumps({"message": "Menu deleted successfully!"}), status=200)


# 메뉴 이미지 전송 api
@app.route("/images/menus/<int:menu_id>", methods=["GET"])
def get_menu_img(menu_id):
    img_path = f"images/menus/{menu_id}.jpg"
    return send_file(img_path, mimetype="image/jpeg")


# 프로필 이미지 전송 api
@app.route("/images/profile/<int:user_id>", methods=["GET"])
def get_profile_img(user_id):
    profile_img = f"images/profile/{user_id}.jpg"
    return send_file(profile_img, mimetype="image/jpeg")


@app.route("/orders", methods=["GET"])
def get_orders():
    return Response(json.dumps({"message": "Your order"}))


@app.route("/orders", methods=["POST"])
def add_order():
    return Response(json.dumps({"message": "Order added successfully!"}))


# 특정 유저 조회 api
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    # 현재 로그인 되어있는 유저가 관리자거나,
    # 조회하려고 하는 유저와 일치한다면 조회하기
    logged_in_user = Users.query.filter_by(email=session.get("email")).first()
    if not logged_in_user:
        return Response(json.dumps({"message": "You must logged in!"}), status=400)
    elif not (user_id == logged_in_user.id or logged_in_user.role == "admin"):
        return Response(
            json.dumps({"message": "You don't have authorize!"}), status=401
        )

    # 만약 유저가 없다면 에러메시지
    user = Users.query.filter_by(id=user_id).first()
    if not user:
        return Response(json.dumps({"message": "User doesn't exist!"}), status=400)
    user = user.to_dict()
    return Response(json.dumps(user, ensure_ascii=False), status=200)


# 새로운 유저 추가 api
@app.route("/users", methods=["POST"])
def add_user():
    # post로부터 데이터를 받아오기
    user_json = request.json

    # password와 pqssword-confirm이 일치하는지 찾기
    if not user_json.get("password") == user_json.get("password-confirm"):
        return Response(
            json.dumps({"message": "Password confirm does not match!"}), status=400
        )

    # email이 이미 가입되어 있는지 확인합니다.
    # 만약 가입되어 있다면 에러 메시지로 응답합니다.
    user = Users.query.filter_by(email=user_json.get("email")).first()
    if user:
        return Response(json.dumps({"message": "User aleady exist!"}), status=400)

    # 새로운 유저를 생성합니다.
    user = Users(
        email=user_json.get("email"),
        password=generate_password_hash(user_json.get("password")),
        role=user_json.get("role"),
        profile_image=user_json.get("profile_image"),
    )

    # db에 저장합니다.
    db.session.add(user)
    db.session.commit()

    return Response(json.dumps({"message": "User added successfully!"}), status=200)


# 유저 삭제 api
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    # 현재 로그인 되어있는 유저가 관리자거나,
    # 삭제하려고 하는 유저와 일치한다면 삭제하기
    logged_in_user = Users.query.filter_by(email=session.get("email")).first()
    if not logged_in_user:
        return Response(json.dumps({"message": "You must logged in!"}), status=400)
    elif not (user_id == logged_in_user.id or logged_in_user.role == "admin"):
        return Response(
            json.dumps({"message": "You don't have authorize!"}), status=401
        )

    # db에서 유저를 찾습니다.
    user = Users.query.filter_by(id=user_id).first()

    # 만약 유저가 없다면 에러 메시지로 응답합니다.
    if not user:
        return Response(json.dumps({"message": "User doesn't exist!"}), status=400)

    # 유저를 삭제하고 db에 적용합니다.
    db.session.delete(user)
    db.session.commit()

    return Response(json.dumps({"message": "User deleted successfully!"}), status=200)


# 로그인 api
@app.route("/api/login", methods=["POST"])
def login():
    # json에서 email과 password를 받아옵니다.
    email = request.json.get("email")
    password = request.json.get("password")

    # email을 기준으로 user를 찾습니다.
    user = Users.query.filter_by(email=email).first()

    # 만약 email과 password가 일치하지 않으면 login fail 메시지를 보냅니다.
    if not user or not check_password_hash(user.password, password):
        return Response(json.dumps({"message": "Login Failed!"}), status=400)

    # 성공 시 login success 메시지를 보냅니다.
    return Response(json.dumps({"message": "Login success!"}), status=200)


# 로그아웃 api
@app.route("/api/logout", methods=["POST"])
def logout():
    return Response(json.dumps({"message": "Logout success!"}), status=200)


# 관리자 회원가입 페이지
@app.route("/admin/register", methods=["GET", "POST"])
def admin_register():

    # post 요청을 받았을 경우
    if request.method == "POST":

        # form에서 data를 받아옵니다.
        data = request.form.to_dict()
        data["role"] = "admin"
        data["profile_image"] = ""

        # 회원가입 api 요청을 보냅니다.
        response = requests.post(
            f"{HOST_IP}/users", headers=app.config["HEADERS"], data=json.dumps(data)
        )

        # 회원가입에 실패하면 에러메시지를 출력합니다.
        if response.status_code == 400:
            flash(response.json().get("message"))
            return redirect(url_for("admin_register"))

        # 회원가입에 성공하면 home으로 리디렉트합니다.
        else:
            return redirect(url_for("home"))

    # get 요청을 받았을 경우
    else:
        return render_template("register.html")


# 관리자 로그인 페이지
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    # post 요청을 받았을 경우
    if request.method == "POST":

        # form에서 data를 받아옵니다.
        data = request.form.to_dict()

        # 로그인 api에 요청을 보냅니다.
        response = requests.post(
            f"{HOST_IP}/api/login", headers=app.config["HEADERS"], data=json.dumps(data)
        )

        # 로그인이 실패하면 실패 메시지를 띄우고, 로그인 화면으로 리디렉트 합니다.
        if response.status_code == 400:
            flash(response.json().get("message"))
            return redirect(url_for("admin_login"))

        # 로그인이 성공하면 세션에 이메일을 등록하고, 홈 화면으로 리디렉트 합니다.
        else:
            session["email"] = data.get("email")
            return redirect(url_for("home"))

    # get 요청을 받았을 경우
    else:
        return render_template("login.html")


# 관리자 로그아웃 페이지
@app.route("/admin/logout", methods=["GET"])
def admin_logout():

    # 로그아웃 api로 요청을 보냅니다.
    response = requests.post(f"{HOST_IP}/api/logout", headers=app.config["HEADERS"])
    if response.status_code == 200:
        session.pop("email", None)
    return redirect(url_for("home"))


# 관리자 페이지
@app.route("/admin", methods=["GET"])
@login_required
def home():
    response = requests.get(f"{HOST_IP}/menus", headers=app.config["HEADERS"])
    datas = response.json()
    return render_template("index.html", email=session.get("email"), datas=datas)


# 관리자 페이지에서 개별 메뉴 조회
@app.route("/admin/menus/<int:menu_id>", methods=["GET"])
@login_required
def admin_get_menu(menu_id):

    # 메뉴 조회 api에 요청을 보냅니다.
    response = requests.get(f"{HOST_IP}/menus/{menu_id}", headers=app.config["HEADERS"])

    # 조회에 실패하면 에러 메시지를 출력합니다.
    if response.status_code == 400:
        flash(response.text)

    # 요청을 json으로 변환해서 data에 저장합니다.
    data = response.json()
    return render_template("menu.html", data=data, email=session.get("email"))


# 관리자 페이지에서 전체 메뉴 다운로드
@app.route("/admin/menus", methods=["GET"])
@login_required
def admin_export_menu():

    # 메뉴 조회 api로 요청을 보냅니다.
    response = requests.get(f"{HOST_IP}/menus", headers=app.config["HEADERS"])

    # 만약 실패한다면 에러 메시지를 출력합니다.
    if response.status_code == 400:
        flash(response.text)

    # json으로 datas를 받아옵니다.
    datas = response.json()

    # datas를 바탕으로 csv 파일을 만듭니다.
    with open("server/datas/menus.csv", "w", encoding="utf-8") as file:
        fieldnames = ["id", "name", "name_en", "kind", "base_price", "type", "img_path"]
        writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(datas)

    # 만든 csv 파일을 보내줍니다.
    return send_file("datas/menus.csv", mimetype="text/csv")


# 관리자 페이지에서 메뉴 추가
@app.route("/admin/menus/add", methods=["GET", "POST"])
@login_required
def admin_add_menu():

    # post 요청을 받았을 경우
    if request.method == "POST":

        # form에서 데이터를 받아옵니다.
        data = request.form.to_dict()
        file = request.files.get("file")

        # 메뉴 추가 api에 요청을 보냅니다.
        response = requests.post(
            f"{HOST_IP}/menus",
            headers={"Authorization": "Bearer token"},
            data=data,
            # files={"file": file.stream},
            files={"file": (file.filename, file.stream, file.content_type)},
        )

        # 만약 실패했다면 에러메시지를 출력합니다.
        if response.status_code == 400:
            flash(response.text)

        return redirect(url_for("home"))

    # get 요청을 받았을 경우
    else:
        return render_template("add_menu.html", email=session.get("email"))


# 관리자 페이지에서 메뉴 수정
@app.route("/admin/menus/<int:menu_id>", methods=["POST"])
@login_required
def admin_update_menu(menu_id):

    # form에서 data를 받아옵니다.
    data = request.form.to_dict()
    file = request.files.get("file")

    # 메뉴 수정 api에 요청을 보냅니다.
    response = requests.put(
        f"{HOST_IP}/menus/{menu_id}",
        headers={"Authorization": "Bearer token"},
        data=data,
        # files={"file": file.stream},
        files={"file": (file.filename, file.stream, file.content_type)},
    )

    # 만약 실패하면 에러 메시지를 출력합니다.
    if response.status_code == 400:
        flash(response.text)

    return redirect(url_for("home"))


# 관리자 페이지에서 메뉴 삭제
@app.route("/admin/menus/<int:menu_id>/delete", methods=["GET"])
@login_required
def admin_delete_menu(menu_id):

    # 메뉴 삭제 api에 요청을 보냅니다.
    response = requests.delete(
        f"{HOST_IP}/menus/{menu_id}", headers=app.config["HEADERS"]
    )

    # 만약 실패하면 에러 메시지를 보냅니다.
    if response.status_code == 400:
        flash(response.text)
    return redirect(url_for("home"))


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


if __name__ == "__main__":
    app.run(debug=True)
