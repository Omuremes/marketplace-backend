from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_offer_service, get_current_admin, get_uow
from app.application.services.offer_service import OfferService
from app.application.dto.offer_dto import OfferCreateDTO, OfferUpdateDTO
from app.application.dto.product_dto import MoneyDTO
from pydantic import BaseModel
from typing import List
from datetime import date
from app.application.uow import UnitOfWork

router = APIRouter()

class AdminOfferResponse(BaseModel):
    id: str
    product_id: str
    seller_id: str
    price: MoneyDTO
    delivery_date: date

@router.get("/products/{product_id}/offers", response_model=List[AdminOfferResponse])
async def list_offers(
    product_id: str,
    current_admin: str = Depends(get_current_admin),
    uow: UnitOfWork = Depends(get_uow)
):
    async with uow:
        offers = await uow.offers.list_by_product_id(product_id)
        return [AdminOfferResponse(
            id=o.id,
            product_id=o.product_id,
            seller_id=o.seller_id,
            price=MoneyDTO(amount=o.price_amount, currency=o.price_currency),
            delivery_date=o.delivery_date
        ) for o in offers]

@router.post("/products/{product_id}/offers", response_model=AdminOfferResponse, status_code=201)
async def create_offer(
    product_id: str,
    data: OfferCreateDTO,
    current_admin: str = Depends(get_current_admin),
    offer_service: OfferService = Depends(get_offer_service)
):
    offer = await offer_service.create_offer(
        product_id=product_id,
        seller_id=data.seller_id,
        price_amount=data.price.amount,
        price_currency=data.price.currency,
        delivery_date=data.delivery_date
    )
    return AdminOfferResponse(
        id=offer.id,
        product_id=offer.product_id,
        seller_id=offer.seller_id,
        price=MoneyDTO(amount=offer.price_amount, currency=offer.price_currency),
        delivery_date=offer.delivery_date
    )

@router.put("/offers/{offer_id}", response_model=AdminOfferResponse)
async def update_offer(
    offer_id: str,
    data: OfferUpdateDTO,
    current_admin: str = Depends(get_current_admin),
    offer_service: OfferService = Depends(get_offer_service)
):
    price_amount = data.price.amount if data.price else None
    price_currency = data.price.currency if data.price else None
    offer = await offer_service.update_offer(
        offer_id=offer_id,
        seller_id=data.seller_id,
        price_amount=price_amount,
        price_currency=price_currency,
        delivery_date=data.delivery_date
    )
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
        
    return AdminOfferResponse(
        id=offer.id,
        product_id=offer.product_id,
        seller_id=offer.seller_id,
        price=MoneyDTO(amount=offer.price_amount, currency=offer.price_currency),
        delivery_date=offer.delivery_date
    )

@router.delete("/offers/{offer_id}", status_code=204)
async def delete_offer(
    offer_id: str,
    current_admin: str = Depends(get_current_admin),
    offer_service: OfferService = Depends(get_offer_service)
):
    deleted = await offer_service.delete_offer(offer_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Offer not found")
