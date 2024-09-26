from fastapi import Path
from typing import Annotated

from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from core.models import db_helper


async def product_by_id(product_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency)):
    product = await crud.get_product(session=session, product_id=product_id)
    if product is not None:
        return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND
    )
