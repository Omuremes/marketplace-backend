from sqlalchemy.ext.asyncio import AsyncSession
from app.application.uow import UnitOfWork
from app.infrastructure.db.session import AsyncSessionLocal
from app.persistence.repositories.product_repo import SqlAlchemyProductRepository
from app.persistence.repositories.seller_repo import SqlAlchemySellerRepository
from app.persistence.repositories.offer_repo import SqlAlchemyOfferRepository
from app.persistence.repositories.admin_repo import SqlAlchemyAdminRepository
from app.persistence.repositories.audit_repo import SqlAlchemyAuditLogRepository

class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory=AsyncSessionLocal):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()
        self.products = SqlAlchemyProductRepository(self.session)
        self.sellers = SqlAlchemySellerRepository(self.session)
        self.offers = SqlAlchemyOfferRepository(self.session)
        self.admins = SqlAlchemyAdminRepository(self.session)
        self.audit_logs = SqlAlchemyAuditLogRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
