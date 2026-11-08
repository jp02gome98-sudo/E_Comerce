
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(80), nullable=False, default="General")
    description = db.Column(db.Text, default="")
    price = db.Column(db.Integer, nullable=False, default=0)
    stock = db.Column(db.Integer, nullable=False, default=0)
    image = db.Column(db.String(255), default="")


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    customer_name = db.Column(
        db.String(100), nullable=False
    )

    customer_email = db.Column(
        db.String(150), nullable=False
    )

    total = db.Column(db.Integer, nullable=False)

    status = db.Column(
        db.String(30),
        default="Pendiente",
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    items = db.relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("order.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id"),
        nullable=True
    )

    product_name = db.Column(
        db.String(150),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    unit_price = db.Column(
        db.Integer,
        nullable=False
    )

    order = db.relationship(
        "Order",
        back_populates="items"
    )
