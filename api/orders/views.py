from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper
from . import crud
from .schemas import OrderCreate, Order
from .dependencies import order_by_id
from fastapi.responses import HTMLResponse
from fastapi import Request

from ...main import templates

router = APIRouter(tags=["Orders"])

@router.post("/", response_class=HTMLResponse)
async def create_order_view(
    request: Request,
    order_in: OrderCreate,
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    order = await crud.create_order(session=session, order_create=order_in)

    return templates.TemplateResponse("index.html", {"request": request, "order": order})


@router.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_in: OrderCreate,
    session: AsyncSession = Depends(db_helper.session_dependency)
) -> Order:
    return await crud.create_order(session=session, order_create=order_in)


@router.get("", response_model=list[Order])
async def get_orders(session: AsyncSession = Depends(db_helper.session_dependency)) -> list[Order]:
    return await crud.get_orders(session=session)


@router.get("/{order_id}", response_model=Order)
async def get_order(order: Order = Depends(order_by_id)):
    return order


@router.patch("/{order_id}/status", response_model=str)
async def update_order_status(
    order_id: int,
    new_status: str,
    session: AsyncSession = Depends(db_helper.session_dependency)
) -> str:
    return await crud.update_order_status(session=session, order_id=order_id, new_status=new_status)

