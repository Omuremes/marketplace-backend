from typing import List, Optional, Dict
from dataclasses import dataclass, field
import uuid
from datetime import date
from .offer import Offer

@dataclass
class Product:
    id: str
    name: str
    price_amount: float
    price_currency: str
    stock: int
    image_object_key: Optional[str] = None
    thumbnail_object_key: Optional[str] = None
    attributes: List[Dict[str, str]] = field(default_factory=list)
    offers: List[Offer] = field(default_factory=list)
    nearest_delivery_date: Optional[date] = None

    @classmethod
    def create(cls, name: str, price_amount: float, price_currency: str, stock: int, attributes: List[Dict[str, str]]) -> "Product":
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            price_amount=price_amount,
            price_currency=price_currency,
            stock=stock,
            attributes=attributes
        )
