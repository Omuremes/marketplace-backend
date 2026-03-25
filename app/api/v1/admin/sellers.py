from fastapi import APIRouter, Depends
from typing import List
from app.api.deps import get_current_admin, get_uow
from app.application.uow import UnitOfWork
from pydantic import BaseModel

router = APIRouter()

class AdminSellerResponse(BaseModel):
    id: str
    name: str
    email: str
    rating: float

@router.get("", response_model=List[AdminSellerResponse])
async def list_sellers(
    current_admin: str = Depends(get_current_admin),
    uow: UnitOfWork = Depends(get_uow)
):
    async with uow:
        sellers = await uow.sellers.list_sellers()
    return [AdminSellerResponse(id=s.id, name=s.name, email=s.email, rating=s.rating) for s in sellers]
