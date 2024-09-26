from fastapi import HTTPException
from sqlalchemy import select, Result, update
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Order, Product, OrderItem
from .schemas import OrderCreate
from typing import List


async def create_order(session: AsyncSession, order_create: OrderCreate) -> Order:
    order_items = []

    for item in order_create.items:
        product = await session.get(Product, item.product_id)
        if product is None:
            raise HTTPException(status_code=404, detail=f"Product with id {item.product_id} not found")

        if product.available_quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough quantity for product id {item.product_id}")

        product.available_quantity -= item.quantity

        order_item = OrderItem(product_id=item.product_id, quantity=item.quantity)
        order_items.append(order_item)

    order = Order(status=order_create.status, order_items=order_items)
    session.add(order)

    session.add_all(order_items)
    await session.commit()
    await session.refresh(order)

    order_response = {
        "id": order.id,
        "status": order.status,
        "created_at": order.created_at.isoformat(),
        "items": [
            {
                "product_id": item.product_id,
                "quantity": item.quantity
            } for item in order.order_items
        ]
    }

    return order_response


async def get_orders(session: AsyncSession) -> List[dict]:
    stmt = select(Order).order_by(Order.id)
    result: Result = await session.execute(stmt)
    orders = result.scalars().all()

    order_responses = []
    for order in orders:
        order_response = {
            "id": order.id,
            "status": order.status,
            "created_at": order.created_at.isoformat(),
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity
                } for item in order.order_items
            ]
        }
        order_responses.append(order_response)

    return order_responses


async def get_order(session: AsyncSession, order_id: int) -> Order:
    order = await session.get(Order, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    order_data = {
        "id": order.id,
        "status": order.status,
        "created_at": order.created_at.isoformat(),
        "items": [
            {
                "product_id": item.product_id,
                "quantity": item.quantity
            } for item in order.order_items
        ]
    }

    return order_data


async def update_order_status(session: AsyncSession, order_id: int, current_status: str) -> str:
    stmt = select(Order.status).where(Order.id == order_id)
    result = await session.execute(stmt)
    order_status = result.scalar_one_or_none()

    if order_status is None:
        raise HTTPException(status_code=404, detail="Order not found")

    if current_status == order_status:
        return "Same status as it was before, please choose a new one"

    update_stmt = (
        update(Order).where(Order.id == order_id).values(status=current_status)
    )
    await session.execute(update_stmt)
    await session.commit()

    return "Status updated"
