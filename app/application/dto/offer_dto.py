from pydantic import BaseModel
from datetime import date
from .product_dto import MoneyDTO

class OfferCreateDTO(BaseModel):
    seller_id: str
    price: MoneyDTO
    delivery_date: date

class OfferUpdateDTO(BaseModel):
    seller_id: str | None = None
    price: MoneyDTO | None = None
    delivery_date: date | None = None
