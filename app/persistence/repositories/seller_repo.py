from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.application.uow import SellerRepository
from app.domain.entities.seller import Seller
from app.infrastructure.db.models import SellerModel
from app.persistence.mappers.product_mapper import DomainMapper

class SqlAlchemySellerRepository(SellerRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, seller: Seller) -> None:
        model = DomainMapper.to_seller_model(seller)
        self.session.add(model)
        await self.session.flush()

    async def list_sellers(self) -> List[Seller]:
        stmt = select(SellerModel).order_by(SellerModel.name)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [DomainMapper.to_seller_domain(m) for m in models]

    async def get_by_id(self, seller_id: str) -> Optional[Seller]:
        model = await self.session.get(SellerModel, seller_id)
        if model:
            return DomainMapper.to_seller_domain(model)
        return None
