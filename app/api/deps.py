from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic import ValidationError
from app.infrastructure.config.settings import settings
from app.infrastructure.db.session import AsyncSessionLocal
from app.infrastructure.db.uow import SqlAlchemyUnitOfWork
from app.application.uow import UnitOfWork
from app.application.services.product_service import ProductService
from app.application.services.offer_service import OfferService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/admin/auth/login")

def get_uow() -> UnitOfWork:
    return SqlAlchemyUnitOfWork(session_factory=AsyncSessionLocal)

def get_product_service(uow: UnitOfWork = Depends(get_uow)) -> ProductService:
    return ProductService(uow)

def get_offer_service(uow: UnitOfWork = Depends(get_uow)) -> OfferService:
    return OfferService(uow)

def get_current_admin(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None or username != settings.ADMIN_USERNAME:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username
