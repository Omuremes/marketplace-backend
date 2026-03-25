import json
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.application.uow import AuditLogRepository
from app.infrastructure.db.models import ProductAuditLogModel

class SqlAlchemyAuditLogRepository(AuditLogRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, admin_id: Optional[str], product_id: str, action: str, changes: Optional[dict] = None) -> None:
        model = ProductAuditLogModel(
            admin_id=admin_id,
            product_id=product_id,
            action=action,
            changes_json=json.dumps(changes) if changes else None
        )
        self.session.add(model)
        await self.session.flush()
