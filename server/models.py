from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

db = SQLAlchemy()


class Status(Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"


class Type(Enum):
    ice = "ice"
    hot = "hot"


class Size(Enum):
    small = "small"
    medium = "medium"
    large = "large"


class Ice(Enum):
    no = "no"
    half = "half"
    normal = "normal"


class Role(Enum):
    user = "user"
    admin = "admin"


# 모델 정의
class Menu(db.Model):
    __tablename__ = "menu"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    name_en = db.Column(db.String(50), nullable=False)
    kind = db.Column(db.String(50), nullable=False)
    base_price = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Enum(Type), nullable=True)
    img_path = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # 모델 클래스를 dict 형태로 변환하는 메소드
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_en": self.name_en,
            "kind": self.kind,
            "base_price": self.base_price,
            "type": self.type.value,
            "img_path": self.img_path,
        }

    def __repr__(self):
        return f"<Menu {self.name}>"


class Orders(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum(Status), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    order_items = db.relationship("OrderItems", backref="order", lazy=True)

    def __repr__(self):
        return f"<Orders {self.id}>"

    # @property
    # def total_price(self):
    #     return sum(item.unit_price for item in self.order_items)


class OrderItems(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey("menu.id"), nullable=False)
    size = db.Column(db.Enum(Size), nullable=False)
    ice = db.Column(db.Enum(Ice), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    # unit_price = db.Column(db.Integer, nullable=False)

    menu = db.relationship("Menu", backref="order_items", lazy=True)

    def __repr__(self):
        return f"<OrderItems {self.id} - {self.menu_id}>"

    @property
    def unit_price(self):
        size_option = 1
        if self.size == Size.MEDIUM:
            size_option *= 1.5
        elif self.size == Size.LARGE:
            size_option *= 2
        return self.menu.base_price * size_option * self.quantity


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(Role), nullable=False)
    profile_image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "role": self.role.value,
            "profile_image": self.profile_image,
        }
