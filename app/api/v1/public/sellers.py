from fastapi import APIRouter, HTTPException, Depends
from app.application.services.auth_service import AuthService
from pydantic import BaseModel
from app.api.deps import get_uow
from app.application.uow import UnitOfWork

router = APIRouter()

class SellerRegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class SellerLoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class SellerPublicDTO(BaseModel):
    id: str
    name: str
    email: str
    rating: float

class SellerRegisterResponse(BaseModel):
    seller: SellerPublicDTO
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=SellerRegisterResponse)
async def register(body: SellerRegisterRequest, uow: UnitOfWork = Depends(get_uow)):
    try:
        seller = await AuthService.register_seller(uow, body.name, body.email, body.password)
        access_token = AuthService.create_access_token(data={"sub": seller.email, "role": "seller"})
        refresh_token = AuthService.create_refresh_token(data={"sub": seller.email, "role": "seller"})
        
        dto = SellerPublicDTO(
            id=seller.id,
            name=seller.name,
            email=seller.email,
            rating=seller.rating
        )
        return SellerRegisterResponse(seller=dto, access_token=access_token, refresh_token=refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponse)
async def login(body: SellerLoginRequest, uow: UnitOfWork = Depends(get_uow)):
    seller = await AuthService.authenticate_seller(uow, body.email, body.password)
    if not seller:
        raise HTTPException(
            status_code=401,
            detail={"error": "unauthorized", "message": "Incorrect email or password"}
        )
    access_token = AuthService.create_access_token(data={"sub": seller.email, "role": "seller"})
    refresh_token = AuthService.create_refresh_token(data={"sub": seller.email, "role": "seller"})
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)
