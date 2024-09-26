from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str
    description: str
    price: int
    available_quantity: int


class ProductCreate(ProductBase):
    status: str
    available_quantity: int
    pass


class ProductUpdate(ProductCreate):
    pass


class ProductUpdatePartial(BaseModel):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    available_quantity: int | None = None
    status: str | None = None


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str
    available_quantity: int


