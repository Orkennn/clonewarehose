from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base


class Product(Base):

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(40))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int] = mapped_column(Integer)
    available_quantity: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String)

    order_items = relationship('OrderItem', back_populates='product', lazy='selectin')






