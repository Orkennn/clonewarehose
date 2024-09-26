from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .schemas import ProductCreate, ProductUpdate, ProductUpdatePartial
from core.models import Product, OrderItem
from typing import Optional, Type
from sqlalchemy import select, Result


async def create_product(session: AsyncSession, product_in: ProductCreate) -> Product:
    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()
    return product


async def get_products(session: AsyncSession) -> list[Product]:
    stmt = select(Product).order_by(Product.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_product(session: AsyncSession, product_id: int) -> Optional[Type[Product]]:
    return await session.get(Product, product_id)


async def update_product(
        session: AsyncSession,
        product_id: int,
        product_update: ProductUpdate | ProductUpdatePartial,
        partial: bool = False,
) -> Product:

    product = await session.get(Product, product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    for name, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, name, value)

    await session.commit()
    await session.refresh(product)

    return product


async def delete_product(
    session: AsyncSession,
    product_id: int,
) -> None:
    product = await session.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    order_items = await session.execute(select(OrderItem).where(OrderItem.product_id == product_id))
    order_items = order_items.scalars().all()

    for item in order_items:
        await session.delete(item)

    await session.delete(product)
    await session.commit()
