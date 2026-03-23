from app.application.uow import UnitOfWork
from app.domain.entities.seller import Seller
from app.infrastructure.auth.jwt import create_access_token
from app.infrastructure.auth.password import verify_password, get_password_hash
from typing import Optional

class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return verify_password(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return get_password_hash(password)

    @staticmethod
    def create_access_token(data: dict) -> str:
        return create_access_token(data)

    @staticmethod
    def create_refresh_token(data: dict) -> str:
        from app.infrastructure.auth.jwt import create_refresh_token
        return create_refresh_token(data)

    @staticmethod
    async def authenticate_admin(uow: UnitOfWork, email: str, password: str) -> bool:
        async with uow:
            admin = await uow.admins.get_by_email(email)
            if not admin:
                return False
            return AuthService.verify_password(password, admin.password_hash)

    @staticmethod
    async def authenticate_seller(uow: UnitOfWork, email: str, password: str) -> Optional[Seller]:
        async with uow:
            seller = await uow.sellers.get_by_email(email)
            if not seller:
                return None
            if not AuthService.verify_password(password, seller.password_hash):
                return None
            return seller

    @staticmethod
    async def register_seller(uow: UnitOfWork, name: str, email: str, password: str) -> Seller:
        async with uow:
            existing = await uow.sellers.get_by_email(email)
            if existing:
                raise ValueError("Seller with this email already exists")
            
            hashed_pw = AuthService.get_password_hash(password)
            seller = Seller.create(name=name, email=email, password_hash=hashed_pw, rating=0.0)
            await uow.sellers.add(seller)
            await uow.commit() # Save changes
            return seller

