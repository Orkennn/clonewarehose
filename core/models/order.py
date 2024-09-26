from typing import List, TYPE_CHECKING
from .base import Base

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

if TYPE_CHECKING:
    from . import OrderItem


class Order(Base):

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String)

    order_items: Mapped[List['OrderItem']] = (relationship('OrderItem',
                                                          back_populates='order',
                                                          lazy='selectin',
                                                          cascade='all, delete-orphan'))
