from typing import Optional
from datetime import date
from app.application.uow import UnitOfWork
from app.domain.entities.offer import Offer

class OfferService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_offer(self, product_id: str, seller_id: str, price_amount: float, price_currency: str, delivery_date: date) -> Offer:
        async with self.uow as uow:
            offer = Offer.create(
                product_id=product_id,
                seller_id=seller_id,
                price_amount=price_amount,
                price_currency=price_currency,
                delivery_date=delivery_date
            )
            await uow.offers.add(offer)
            await uow.commit()
            return offer

    async def update_offer(self, offer_id: str, seller_id: Optional[str] = None, price_amount: Optional[float] = None, price_currency: Optional[str] = None, delivery_date: Optional[date] = None) -> Optional[Offer]:
        async with self.uow as uow:
            offer = await uow.offers.get_by_id(offer_id)
            if not offer:
                return None
            
            if seller_id is not None: 
                offer.seller_id = seller_id
            if price_amount is not None:    
                offer.price_amount = price_amount
            if price_currency is not None: 
                offer.price_currency = price_currency
            if delivery_date is not None: 
                offer.delivery_date = delivery_date
            
            await uow.offers.update(offer)
            await uow.commit()
            return offer

    async def delete_offer(self, offer_id: str) -> bool:
        async with self.uow as uow:
            offer = await uow.offers.get_by_id(offer_id)
            if not offer:
                return False
            await uow.offers.delete(offer_id)
            await uow.commit()
            return True
