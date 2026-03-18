from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_uow, get_current_admin
from app.application.uow import UnitOfWork
from app.domain.entities.seller import Seller
from app.application.dto.product_dto import SellerDTO
from pydantic import BaseModel
from typing import List

router = APIRouter()

class AdminSellerCreate(BaseModel):
    name: str
    rating: float

@router.get("", response_model=List[SellerDTO])
async def list_sellers(
    current_admin: str = Depends(get_current_admin),
    uow: UnitOfWork = Depends(get_uow)
):
    async with uow:
        sellers = await uow.sellers.list_sellers()
        return [SellerDTO(id=s.id, name=s.name, rating=s.rating) for s in sellers]

@router.post("", response_model=SellerDTO, status_code=201)
async def create_seller(
    data: AdminSellerCreate,
    current_admin: str = Depends(get_current_admin),
    uow: UnitOfWork = Depends(get_uow)
):
    async with uow:
        seller = Seller.create(name=data.name, rating=data.rating)
        await uow.sellers.add(seller)
        await uow.commit()
        return SellerDTO(id=seller.id, name=seller.name, rating=seller.rating)
