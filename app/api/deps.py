from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from pydantic import ValidationError
from app.infrastructure.config.settings import settings
from app.infrastructure.db.session import AsyncSessionLocal
from app.infrastructure.db.uow import SqlAlchemyUnitOfWork
from app.infrastructure.auth.jwt import decode_access_token
from app.application.uow import UnitOfWork
from app.application.services.product_service import ProductService
from app.application.services.offer_service import OfferService

security = HTTPBearer()

def get_uow() -> UnitOfWork:
    return SqlAlchemyUnitOfWork(session_factory=AsyncSessionLocal)

def get_product_service(uow: UnitOfWork = Depends(get_uow)) -> ProductService:
    return ProductService(uow)

def get_offer_service(uow: UnitOfWork = Depends(get_uow)) -> OfferService:
    return OfferService(uow)

async def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security), uow: UnitOfWork = Depends(get_uow)) -> str:
    try:
        payload = decode_access_token(credentials.credentials)
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None or role != "admin":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate admin credentials")
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    async with uow:
        admin = await uow.admins.get_by_email(email)
        if not admin:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin not found")
    return admin.id

async def get_current_seller(credentials: HTTPAuthorizationCredentials = Depends(security), uow: UnitOfWork = Depends(get_uow)) -> str:
    try:
        payload = decode_access_token(credentials.credentials)
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None or role != "seller":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate seller credentials")
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    async with uow:
        seller = await uow.sellers.get_by_email(email)
        if not seller:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Seller not found")
    return seller.email

