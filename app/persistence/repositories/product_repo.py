from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import List, Optional
from app.application.uow import ProductRepository
from app.domain.entities.product import Product
from app.infrastructure.db.models import ProductModel, OfferModel


class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, product: Product) -> None:
        model = DomainMapper.to_product_model(product)
        self.session.add(model)
        await self.session.flush()

    async def get_by_id(self, product_id: str) -> Optional[Product]:
        stmt = (
            select(ProductModel)
            .where(ProductModel.id == product_id)
            .options(
                selectinload(ProductModel.offers).selectinload(OfferModel.seller),
                selectinload(ProductModel.attributes)
            )
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            return DomainMapper.to_product_domain(model)
        return None

    async def list_products(self, limit: int, cursor: Optional[str] = None) -> List[Product]:
        stmt = (
            select(ProductModel)
            .options(
                selectinload(ProductModel.offers).selectinload(OfferModel.seller),
                selectinload(ProductModel.attributes)
            )
            .order_by(ProductModel.id)
            .limit(limit)
        )
        if cursor:
            stmt = stmt.where(ProductModel.id > cursor)

        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [DomainMapper.to_product_domain(m) for m in models]

    async def count_products(self) -> int:
        stmt = select(func.count(ProductModel.id))
        result = await self.session.execute(stmt)
        return result.scalar()

    async def update(self, product: Product) -> None:
        model = DomainMapper.to_product_model(product)
        await self.session.merge(model)
        await self.session.flush()

    async def delete(self, product_id: str) -> None:
        model = await self.session.get(ProductModel, product_id)
        if model:
            await self.session.delete(model)
            await self.session.flush()


from app.persistence.mappers.product_mapper import DomainMapper
