from fastapi import APIRouter

from .products.views import router as products_router
from .orders.views import router as orders_router

router = APIRouter()
router.include_router(router=products_router, prefix="/products")
router.include_router(router=orders_router, prefix="/orders")
