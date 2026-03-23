from typing import List, Optional, Dict, Any
from app.application.uow import UnitOfWork
from app.domain.entities.product import Product
from app.infrastructure.storage.minio_client import get_storage_client
from app.application.dto.product_dto import (
    ProductListItemDTO, ProductDetailsDTO, ProductAttributeDTO,
    MoneyDTO, PublicOfferDTO, SellerDTO
)

class ProductService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.storage_client = get_storage_client()

    async def list_products(
        self,
        limit: int = 20,
        cursor: Optional[str] = None,
        search: Optional[str] = None,
    ) -> tuple[List[ProductListItemDTO], str | None]:
        async with self.uow as uow:
            # Fetch one extra row to determine whether next page exists.
            products = await uow.products.list_products(limit=limit + 1, cursor=cursor, search=search)

            has_next_page = len(products) > limit
            page_products = products[:limit]

            dtos = []
            for p in page_products:
                thumb_url = self.storage_client.get_file_url(p.thumbnail_object_key) if p.thumbnail_object_key else None
                dtos.append(ProductListItemDTO(
                    id=p.id,
                    name=p.name,
                    thumbnail_url=thumb_url,
                    price=MoneyDTO(amount=p.price_amount, currency=p.price_currency),
                    stock=p.stock,
                    nearest_delivery_date=p.nearest_delivery_date
                ))

            next_cursor = page_products[-1].id if has_next_page and page_products else None
            return dtos, next_cursor

    async def get_product_details(self, product_id: str, offers_sort: str = "price") -> Optional[ProductDetailsDTO]:
        async with self.uow as uow:
            product = await uow.products.get_by_id(product_id)
            if not product:
                return None

            offers = list(product.offers)
            if offers_sort == "price":
                offers.sort(key=lambda o: o.price_amount)
            elif offers_sort == "delivery_date":
                offers.sort(key=lambda o: o.delivery_date)

            offer_dtos = []
            for o in offers:
                if o.seller:
                    seller_dto = SellerDTO(id=o.seller.id, name=o.seller.name, rating=o.seller.rating)
                    offer_dtos.append(PublicOfferDTO(
                        id=o.id,
                        seller=seller_dto,
                        price=MoneyDTO(amount=o.price_amount, currency=o.price_currency),
                        delivery_date=o.delivery_date,
                    ))

            attribute_dtos = [
                ProductAttributeDTO(key=attr.get("key", ""), value=attr.get("value", ""))
                for attr in product.attributes
            ]

            img_url = self.storage_client.get_file_url(product.image_object_key) if product.image_object_key else None

            return ProductDetailsDTO(
                id=product.id,
                name=product.name,
                image_url=img_url,
                attributes=attribute_dtos,
                offers=offer_dtos,
            )

    async def get_product_raw(self, product_id: str) -> Optional[Product]:
        """Returns full domain entity including stock (used by admin endpoints)."""
        async with self.uow as uow:
            return await uow.products.get_by_id(product_id)

    async def create_product(self, name: str, price_amount: float, price_currency: str, stock: int, attributes: List[Dict[str, str]]) -> Product:
        async with self.uow as uow:
            product = Product.create(name=name, price_amount=price_amount, price_currency=price_currency, stock=stock, attributes=attributes)
            await uow.products.add(product)
            await uow.commit()
            return product

    async def update_product(self, product_id: str, updates: Dict[str, Any]) -> Optional[Product]:
        async with self.uow as uow:
            product = await uow.products.get_by_id(product_id)
            if not product:
                return None
                
            if "name" in updates: 
                product.name = updates["name"]
            if "price_amount" in updates: 
                product.price_amount = updates["price_amount"]
            if "price_currency" in updates: 
                product.price_currency = updates["price_currency"]
            if "stock" in updates: 
                product.stock = updates["stock"]
            if "attributes" in updates: 
                product.attributes = updates["attributes"]
            
            await uow.products.update(product)
            await uow.commit()
            return product

    async def delete_product(self, product_id: str) -> bool:
        async with self.uow as uow:
            product = await uow.products.get_by_id(product_id)
            if not product:
                return False
            await uow.products.delete(product_id)
            await uow.commit()
            return True

    async def update_image(self, product_id: str, image_object_key: str, thumbnail_object_key: str) -> Optional[Product]:
        async with self.uow as uow:
            product = await uow.products.get_by_id(product_id)
            if not product:
                return None
            product.image_object_key = image_object_key
            product.thumbnail_object_key = thumbnail_object_key
            await uow.products.update(product)
            await uow.commit()
            return product
