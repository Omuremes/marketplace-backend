from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import date

class MoneyDTO(BaseModel):
    amount: float
    currency: str

class ProductAttributeDTO(BaseModel):
    key: str
    value: str

class SellerDTO(BaseModel):
    id: str
    name: str
    rating: float

# Public Offer: matches OpenAPI Offer schema (id, seller, price, delivery_date)
class PublicOfferDTO(BaseModel):
    id: str
    seller: SellerDTO
    price: MoneyDTO
    delivery_date: date

# Internal DTO used in services (includes product_id / seller_id)
class OfferDTO(BaseModel):
    id: str
    product_id: str
    seller_id: str
    price: MoneyDTO
    delivery_date: date

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
    offers: List[PublicOfferDTO]
