# Kiosk application

## 개요

서버-클라이언트 모델로 작동하는 키오스크 어플리케이션

## 목차

- [API 구조](#api-구조)
- [DB 스키마](#db-스키마)
- [To-Do List](#to-do-list)
- [코드 컨벤션](#코드-컨벤션)
- [패키지 구조](#패키지-구조)
- [기술 스택](#기술-스택)
- [실행 방법](#실행-방법)
- [트러블슈팅](#트러블슈팅)

## API 구조

REST API로 작성하였으며, Menu와 Order 리소스에 관한 CRUD 기능을 구현한다.

### Menu 관련

- **GET** `/menus`
  → 메뉴 리스트를 가져옵니다.
- **GET** `/menus/:id`
  → 특정 메뉴의 정보를 가져옵니다.
- **POST** `/menus`
  → 새로운 메뉴를 추가합니다.
- **PUT** `/menus/:id`
  → 특정 메뉴를 수정합니다.
- **DELETE** `/menus/:id`
  → 특정 메뉴를 삭제합니다.

### Order 관련

- **GET** `/orders`
  → 주문 내역을 가져옵니다.
- **POST** `/orders`
  → 새로운 주문을 생성합니다.
- **PUT** `/orders/:id`
  → 특정 주문을 수정합니다.

### Image 관련

- **GET** `/images/menus/:id`
  → 메뉴 이미지를 가져옵니다.
- **GET** `/images/profile/:id`
  → 프로필 이미지를 가져옵니다.

### User 관련

- **GET** `/users/:id`
  → 특정 사용자를 조회합니다.
- **POST** `/users`
  → 새로운 사용자를 생성합니다.
- **DELETE** `/users/:id`
  → 특정 유저를 삭제합니다.

### Login 관련

- **POST** `/api/login`
  → 로그인한 사용자의 세션을 저장합니다.
- **POST** `/api/logout`
  → 로그아웃한 사용자의 세션을 제거합니다.

### Admin 관련

- **GET** `/admin`
  → 관리자 페이지의 홈 페이지입니다.
- **GET, POST** `/admin/register`
  → 관리자 회원가입 페이지입니다.
- **GET, POST** `/admin/login`
  → /api/login을 호출하고 홈 페이지로 리다이렉트 합니다.
- **POST** `/admin/logout`
  → /api/logout을 호출하고 홈 페이지로 리다이렉트 합니다.
- **GET, POST** `/admin/:id`
  → 관리자 유저의 프로필입니다.
- **GET** `/admin/menus`
  → GET /menus를 호출해서 전체 메뉴를 csv 파일로 다운받을 수 있습니다.
- **POST** `/admin/menus`
  → POST /menus를 호출해서 새로운 메뉴를 등록할 수 있습니다.
- **GET** `/admin/menus/:id`
  → GET /menus/:id를 호출해서 id를 통해 특정 메뉴를 조회할 수 있습니다.
- **POST** `/admin/menus/:id`
  → PUT /menus/:id를 호출해서 id를 통해 특정 메뉴를 업데이트 할 수 있습니다.
- **GET** `/admin/menus/:id/delete`
  → POST /menus/:id를 호출해서 id를 통해 특정 메뉴를 삭제 할 수 있습니다.

## DB 스키마

![DB diagram](./assets/diagram.png)

## To-Do List

- [x] **Menu tab bar**: 메뉴화면 탭 바 구현
- [x] **GET /images/:id**: 이미지 처리 로직 구현
- [x] **유저**: 회원가입, 로그인, 로그아웃 기능 구현
- [x] **GET /menus/:id**: 특정 메뉴 불러오기 구현
- [x] **관리자 페이지**: 관리자 페이지 기능들 구현
- [x] **다운로드 기능**: 전체 메뉴를 csv파일로 export
- [ ] **마이페이지**: 관리자 정보 페이지 구현
- [ ] **업로드 기능**: 음식과 유저의 사진 업로드 기능 구현
- [ ] **Electron UI, UX 구현**: 클라이언트 로직 구현
- [ ] **이미지 처리**: 사이즈 조절, 누끼 따기
- [ ] **서버사이드 예외처리**: 오류 처리 로직 구현
- [ ] **GET /orders**: 주문 내역을 가져오는 API 구현
- [ ] **POST /orders**: 새로운 주문을 생성하는 API 구현
- [ ] **PUT /orders**: 주문 수정 API 구현
- [ ] **html, css 주석**: 주석 추가
- [ ] **css의 commit 클래스 리팩토링**: 코드 정리

## 코드 컨벤션

| 적용 대상                    | 컨벤션               |
| ---------------------------- | -------------------- |
| Class, Exception             | **PascalCase**       |
| Function, Variable, DB Table | **snake_case**       |
| CSS Class                    | **kebab-case**       |
| Constant                     | **UPPER_SNAKE_CASE** |
| Indent                       | **Tab**              |
| JS variable                  | **camelCase**        |

## 패키지 구조

```
├── 📁 assets
├── 📁 client
│   ├── 📁 styles / Style sheets
│   │   ├── 📁 components  / Components style sheets
│   │   └── 📁 screens / Screen style sheets
│   ├── index.html / Web entry
│   ├── render.js / Electron renderer processer entry
│   └── main.js / Electron main processer entry
├── 📁 server
│   ├── 📁 images / Contain jpg file
│   ├── app.py / Flask app
│   ├── models.py / ORM model
│   ├── request.py / HTTP request test
│   ├── config.py / Initial option
│   ├── scrape.py / Scrape data from ---- coffee hompage (sorry)
│   └── requirements.txt / Package Dependency
├── README.md
```

## 기술 스택

- **Flask**: Python 기반의 경량 웹 프레임워크로, 빠른 개발과 REST API 구축에 적합합니다.
- **MySQL**: 관계형 데이터베이스로, 주문 및 메뉴 데이터를 효율적으로 관리합니다.
- **HTML, CSS**: 사용자 인터페이스를 구축하기 위한 기본 웹 기술입니다.
- **Electron**: 데스크탑 환경에서 웹 기반 UI를 제공하는 Node.js 패키지입니다.

## 실행 방법

### 공통

1. **Clone repository**

```
git clone https://github.com/AlpacaMale/kiosk
```

### Flask server

1. **Install dependency**

```
pip install -r server/requirements.txt
```

2. **Run flask server**

```
python server/app.py
```

### Electron Client

1. **Move directory**

```
cd client
```

2. **Install dependency**

```
npm i
```

3. **Run electron**

```
npm run start
```

## 트러블슈팅

### JSON 인코딩 문제 해결

response.data 에 들어온 JSON 응답이 인코딩이 깨져서 들어왔다.

```
 "name": "\uc544\uba54\ub9ac\uce74\ub178"
```

jsonify를 설정하기 위해서 JSON_AS_ASCII = False 설정을 넣었으나 제대로 작동이 되지 않아
그냥 json 모듈을 사용해서 ensure_ascii=False 옵션을 주고 Response를 같이 사용해서 응답하였다.

### git bash 환경 변수 문제 해결

git bash 에서 python 버전이 달라서 윈도우 환경 변수의 패스를 자꾸 건드려 보았으나 효과가 없었다.
~/ 디렉토리의 .bashrc와 .bash_profile 을 편집하여 환경변수를 등록, 저장, 적용해서 해결하였다.

### api를 이용한 로그인중 세션 문제 해결

함수 안에서 api를 requests로 호출하는 식으로 로그인 api 로직을 짯는데, api 로직 안에서 세션을 저장하니까 클라이언트 사이드에 쿠키가 생기는게 아니라 서버에 쿠키가 생기는걸 알아차리지 못했다.
api에서는 status_code로 로그인이 성공인지 실패인지만 알려주고, 세션에 저장하는것은 함수에서 처리하니까 해결이 되었다.
