from flask_sqlalchemy import SQLAlchemy
from enum import Enum

db = SQLAlchemy()


# 모델 정의
class Menu(db.Model):
    __tablename__ = "menu"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    name_en = db.Column(db.String(50), nullable=False)
    kind = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(20), nullable=True)
    size = db.Column(db.String(20), nullable=True)
    ice = db.Column(db.String(20), nullable=True)
    img_path = db.Column(db.String(255), nullable=False)

    # 모델 클래스를 dict 형태로 변환하는 메소드
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_en": self.name_en,
            "kind": self.kind,
            "price": self.price,
            "type": self.type.split(", ") if self.type else None,
            "size": self.size.split(", ") if self.size else None,
            "ice": self.ice.split(", ") if self.ice else None,
            "img_path": self.img_path,
        }

    def __repr__(self):
        return f"<Menu {self.name}>"


class Status(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


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
    size = db.Column(db.String(20), nullable=True)
    ice = db.Column(db.String(20), nullable=True)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    # unit_price = db.Column(db.Integer, nullable=False)

    menu = db.relationship("Menu", backref="order_items", lazy=True)

    def __repr__(self):
        return f"<OrderItems {self.id} - {self.menu_id}>"

    @property
    def unit_price(self):
        return self.menu.price * self.quantity if self.menu else 0
