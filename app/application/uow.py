import abc
from app.domain.entities.product import Product
from app.domain.entities.seller import Seller
from app.domain.entities.offer import Offer
from app.domain.entities.admin import Admin
from typing import List, Optional

class ProductRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, product: Product) -> None:
        pass

    @abc.abstractmethod
    async def get_by_id(self, product_id: str) -> Optional[Product]:
        pass

    @abc.abstractmethod
    async def list_products(
        self,
        limit: int,
        cursor: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[Product]:
        pass
        
    @abc.abstractmethod
    async def count_products(self) -> int:
        pass

    @abc.abstractmethod
    async def update(self, product: Product) -> None:
        pass

    @abc.abstractmethod
    async def delete(self, product_id: str) -> None:
        pass

class SellerRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, seller: Seller) -> None:
        pass

    @abc.abstractmethod
    async def list_sellers(self) -> List[Seller]:
        pass

    @abc.abstractmethod
    async def get_by_email(self, email: str) -> Optional[Seller]:
        pass

class AdminRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, admin: Admin) -> None:
        pass

    @abc.abstractmethod
    async def get_by_email(self, email: str) -> Optional[Admin]:
        pass

class OfferRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, offer: Offer) -> None:
        pass
        
    @abc.abstractmethod
    async def update(self, offer: Offer) -> None:
        pass
        
    @abc.abstractmethod
    async def delete(self, offer_id: str) -> None:
        pass
        
    @abc.abstractmethod
    async def list_by_product_id(self, product_id: str) -> List[Offer]:
        pass

class AuditLogRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, admin_id: Optional[str], product_id: str, action: str, changes: Optional[dict] = None) -> None:
        pass

class UnitOfWork(abc.ABC):
    products: ProductRepository
    sellers: SellerRepository
    offers: OfferRepository
    admins: AdminRepository
    audit_logs: AuditLogRepository

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()

    @abc.abstractmethod
    async def commit(self):
        pass

    @abc.abstractmethod
    async def rollback(self):
        pass

