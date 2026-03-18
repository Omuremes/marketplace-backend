from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Any
from datetime import date

class MoneyDTO(BaseModel):
    amount: float
    currency: str

class ProductAttributeDTO(BaseModel):
    key: str
    value: str

class OfferDTO(BaseModel):
    id: str
    product_id: str
    seller_id: str
    price: MoneyDTO
    delivery_date: date

class SellerDTO(BaseModel):
    id: str
    name: str
    rating: float

class OfferWithSellerDTO(OfferDTO):
    seller: Optional[SellerDTO] = None

class ProductListItemDTO(BaseModel):
    id: str
    name: str
    thumbnail_url: Optional[HttpUrl] = None
    price: MoneyDTO
    stock: int
    nearest_delivery_date: Optional[date] = None

class ProductDetailsDTO(BaseModel):
    id: str
    name: str
    image_url: Optional[HttpUrl] = None
    attributes: List[ProductAttributeDTO]
    offers: List[OfferWithSellerDTO]
