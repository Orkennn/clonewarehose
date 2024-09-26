from fastapi import Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from core.models import db_helper
from .schemas import Order
from typing import Annotated


async def order_by_id(
    order_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency)
) -> Order:
    order = await crud.get_order(session=session, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
