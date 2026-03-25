from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from app.api.deps import get_product_service, get_current_admin
from app.application.services.product_service import ProductService
from app.application.dto.product_dto import ProductAttributeDTO, MoneyDTO
from app.infrastructure.storage.minio_client import get_storage_client, MinioStorageClient
from typing import List, Optional
from pydantic import BaseModel, HttpUrl

router = APIRouter()

class AdminProductCreate(BaseModel):
    name: str
    price: MoneyDTO
    stock: int
    attributes: List[ProductAttributeDTO]

class AdminProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[MoneyDTO] = None
    stock: Optional[int] = None
    attributes: Optional[List[ProductAttributeDTO]] = None

class AdminProductResponse(BaseModel):
    id: str
    name: str
    price: MoneyDTO
    stock: int
    image_url: Optional[HttpUrl] = None
    thumbnail_url: Optional[HttpUrl] = None
    attributes: List[ProductAttributeDTO]

class ImageUploadResponse(BaseModel):
    image_url: HttpUrl
    thumbnail_url: HttpUrl

@router.get("", response_model=dict)
async def list_products(
    limit: int = Query(50, ge=1, le=100),
    cursor: Optional[str] = Query(None),
    search: Optional[str] = Query(None, min_length=1),
    current_admin: str = Depends(get_current_admin),
    product_service: ProductService = Depends(get_product_service)
):
    dtos, next_cursor = await product_service.list_products(limit=limit, cursor=cursor, search=search)
    
    admin_dtos = []
    for dto in dtos:
        # We need attributes for admin list too based on OpenAPI
        # the list_products doesn't return attributes in ProductListItemDTO
        # For simplicity, we fetch details or extend ProductListItemDTO.
        product = await product_service.get_product_details(dto.id)
        if product:
             admin_dtos.append(AdminProductResponse(
                 id=product.id,
                 name=product.name,
                 price=dto.price,
                 stock=dto.stock,
                 image_url=product.image_url,
                 thumbnail_url=dto.thumbnail_url,
                 attributes=product.attributes
             ))
    return {"items": admin_dtos, "next_cursor": next_cursor}

@router.post("", response_model=AdminProductResponse, status_code=201)
async def create_product(
    data: AdminProductCreate,
    current_admin: str = Depends(get_current_admin),
    product_service: ProductService = Depends(get_product_service)
):
    attr_dicts = [{"key": a.key, "value": a.value} for a in data.attributes]
    product = await product_service.create_product(
        name=data.name,
        price_amount=data.price.amount,
        price_currency=data.price.currency,
        stock=data.stock,
        attributes=attr_dicts,
        admin_id=current_admin
    )
    return AdminProductResponse(
        id=product.id,
        name=product.name,
        price=data.price,
        stock=product.stock,
        attributes=data.attributes
    )

@router.get("/{product_id}", response_model=AdminProductResponse)
async def get_product(
    product_id: str,
    current_admin: str = Depends(get_current_admin),
    product_service: ProductService = Depends(get_product_service),
    storage_client: MinioStorageClient = Depends(get_storage_client)
):
    raw_product = await product_service.get_product_raw(product_id)
    if not raw_product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    attr_dtos = [ProductAttributeDTO(key=a.get("key", ""), value=a.get("value", "")) for a in raw_product.attributes]
    image_url = storage_client.get_file_url(raw_product.image_object_key) if raw_product.image_object_key else None
    thumbnail_url = storage_client.get_file_url(raw_product.thumbnail_object_key) if raw_product.thumbnail_object_key else None
    
    return AdminProductResponse(
        id=raw_product.id,
        name=raw_product.name,
        price=MoneyDTO(amount=raw_product.price_amount, currency=raw_product.price_currency),
        stock=raw_product.stock,
        image_url=image_url,
        thumbnail_url=thumbnail_url,
        attributes=attr_dtos
    )

@router.put("/{product_id}", response_model=AdminProductResponse)
async def update_product(
    product_id: str,
    data: AdminProductUpdate,
    current_admin: str = Depends(get_current_admin),
    product_service: ProductService = Depends(get_product_service),
    storage_client: MinioStorageClient = Depends(get_storage_client)
):
    updates = {}
    if data.name is not None: 
        updates["name"] = data.name
    if data.price is not None:
        updates["price_amount"] = data.price.amount
        updates["price_currency"] = data.price.currency
    if data.stock is not None: 
        updates["stock"] = data.stock
    if data.attributes is not None:
        updates["attributes"] = [{"key": a.key, "value": a.value} for a in data.attributes]
        
    product = await product_service.update_product(product_id, updates, admin_id=current_admin)
    if not product:
         raise HTTPException(status_code=404, detail="Product not found")
         
    attr_dtos = [ProductAttributeDTO(key=a.get("key",""), value=a.get("value","")) for a in product.attributes]
    image_url = storage_client.get_file_url(product.image_object_key) if product.image_object_key else None
    thumbnail_url = storage_client.get_file_url(product.thumbnail_object_key) if product.thumbnail_object_key else None
    
    return AdminProductResponse(
        id=product.id,
        name=product.name,
        price=MoneyDTO(amount=product.price_amount, currency=product.price_currency),
        stock=product.stock,
        image_url=image_url,
        thumbnail_url=thumbnail_url,
        attributes=attr_dtos
    )

@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: str,
    current_admin: str = Depends(get_current_admin),
    product_service: ProductService = Depends(get_product_service)
):
    deleted = await product_service.delete_product(product_id, admin_id=current_admin)
    if not deleted:
         raise HTTPException(status_code=404, detail="Product not found")

from io import BytesIO
from PIL import Image

@router.post("/{product_id}/image", response_model=ImageUploadResponse)
async def upload_product_image(
    product_id: str,
    file: UploadFile = File(...),
    current_admin: str = Depends(get_current_admin),
    product_service: ProductService = Depends(get_product_service),
    storage_client: MinioStorageClient = Depends(get_storage_client)
):
    content = await file.read()
    object_key = storage_client.upload_file(file.filename, content, file.content_type)
    
    # Generate thumbnail
    try:
        img = Image.open(BytesIO(content))
        # Convert to RGB to ensure saving as JPEG/PNG works properly for some types
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img.thumbnail((150, 150))
        thumb_io = BytesIO()
        img.save(thumb_io, format="JPEG")
        thumb_content = thumb_io.getvalue()
        
        parts = file.filename.rsplit(".", 1)
        thumb_filename = f"{parts[0]}_thumb.jpg" if len(parts) > 1 else f"{file.filename}_thumb.jpg"
        thumb_object_key = storage_client.upload_file(thumb_filename, thumb_content, "image/jpeg")
    except Exception as e:
        print(f"Thumbnail generation failed: {e}")
        thumb_object_key = object_key
        
    product = await product_service.update_image(product_id, object_key, thumb_object_key, admin_id=current_admin)
    if not product:
         raise HTTPException(status_code=404, detail="Product not found")
         
    url = storage_client.get_file_url(object_key)
    thumb_url = storage_client.get_file_url(thumb_object_key)
    return ImageUploadResponse(image_url=url, thumbnail_url=thumb_url)
