from models import db
import os


class Config:
    SESSION_TYPE = "sqlalchemy"
    SESSION_SQLALCHEMY = db
    SESSION_SQLALCHEMY_TABLE = "session"
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SESSION_COOKIE_DOMAIN = "127.0.0.1"
    SESSION_COOKIE_SECURE = False
    SESSION_PERMANENT = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    HEADERS = {"Content-Type": "application/json; charset=utf-8"}
    JSON_AS_ASCII = False
