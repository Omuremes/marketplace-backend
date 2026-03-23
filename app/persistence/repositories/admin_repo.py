from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.application.uow import AdminRepository
from app.domain.entities.admin import Admin
from app.infrastructure.db.models import AdminModel
from app.persistence.mappers.product_mapper import DomainMapper

class SqlAlchemyAdminRepository(AdminRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, admin: Admin) -> None:
        model = DomainMapper.to_admin_model(admin)
        self.session.add(model)
        await self.session.flush()

    async def get_by_email(self, email: str) -> Optional[Admin]:
        stmt = select(AdminModel).where(AdminModel.email == email)
        result = await self.session.execute(stmt)
        model = result.scalars().first()
        if model:
            return DomainMapper.to_admin_domain(model)
        return None
