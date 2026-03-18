from dataclasses import dataclass
import uuid
from datetime import date
from .seller import Seller

@dataclass
class Offer:
    id: str
    product_id: str
    seller_id: str
    price_amount: float
    price_currency: str
    delivery_date: date
    seller: Seller = None

    @classmethod
    def create(cls, product_id: str, seller_id: str, price_amount: float, price_currency: str, delivery_date: date) -> "Offer":
        return cls(
            id=str(uuid.uuid4()),
            product_id=product_id,
            seller_id=seller_id,
            price_amount=price_amount,
            price_currency=price_currency,
            delivery_date=delivery_date
        )
