from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from app.application.uow import OfferRepository
from app.domain.entities.offer import Offer
from app.infrastructure.db.models import OfferModel
from app.persistence.mappers.product_mapper import DomainMapper

class SqlAlchemyOfferRepository(OfferRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, offer: Offer) -> None:
        model = DomainMapper.to_offer_model(offer)
        self.session.add(model)
        await self.session.flush()

    async def update(self, offer: Offer) -> None:
        model = DomainMapper.to_offer_model(offer)
        await self.session.merge(model)
        await self.session.flush()

    async def delete(self, offer_id: str) -> None:
        model = await self.session.get(OfferModel, offer_id)
        if model:
            await self.session.delete(model)
            await self.session.flush()

    async def list_by_product_id(self, product_id: str) -> List[Offer]:
        stmt = (
            select(OfferModel)
            .where(OfferModel.product_id == product_id)
            .options(selectinload(OfferModel.seller))
            .order_by(OfferModel.price_amount)
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [DomainMapper.to_offer_domain(m) for m in models]
        
    async def get_by_id(self, offer_id: str) -> Optional[Offer]:
        stmt = (
            select(OfferModel)
            .where(OfferModel.id == offer_id)
            .options(selectinload(OfferModel.seller))
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            return DomainMapper.to_offer_domain(model)
        return None
