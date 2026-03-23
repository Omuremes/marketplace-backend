from fastapi import APIRouter, Depends, HTTPException, Query
from app.api.deps import get_product_service
from app.application.services.product_service import ProductService
from app.application.dto.product_dto import ProductListItemDTO, ProductDetailsDTO
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

class PaginatedProducts(BaseModel):
    items: List[ProductListItemDTO]
    next_cursor: Optional[str] = None

@router.get("", response_model=PaginatedProducts)
async def list_public_products(
    limit: int = Query(20, ge=1, le=100),
    cursor: Optional[str] = Query(None, description="Cursor for pagination"),
    search: Optional[str] = Query(None, min_length=1, description="Case-insensitive search by product name"),
    product_service: ProductService = Depends(get_product_service)
):
    dtos, next_cursor = await product_service.list_products(limit=limit, cursor=cursor, search=search)
    return PaginatedProducts(items=dtos, next_cursor=next_cursor)

@router.get("/{product_id}", response_model=ProductDetailsDTO)
async def get_product_details(
    product_id: str,
    offers_sort: str = Query("price", regex="^(price|delivery_date)$"),
    product_service: ProductService = Depends(get_product_service)
):
    details = await product_service.get_product_details(product_id=product_id, offers_sort=offers_sort)
    if not details:
        raise HTTPException(status_code=404, detail="Product not found")
    return details
