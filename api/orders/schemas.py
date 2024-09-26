from pydantic import BaseModel, ConfigDict
from typing import List


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderBase(BaseModel):
    status: str


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class Order(OrderBase):
    id: int
    created_at: str
    items: List[OrderItemCreate]

    model_config = ConfigDict(from_attributes=True)
