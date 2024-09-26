from sqlalchemy import  Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base


class OrderItem(Base):

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.id'))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'))
    quantity: Mapped[int] = mapped_column(Integer)

    order = relationship('Order', back_populates='order_items')
    product = relationship('Product', back_populates='order_items')