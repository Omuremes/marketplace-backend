from typing import List, Optional, Dict, Any
from app.application.uow import UnitOfWork
from app.domain.entities.product import Product
from app.application.dto.product_dto import ProductListItemDTO, ProductDetailsDTO, ProductAttributeDTO, MoneyDTO, OfferWithSellerDTO, SellerDTO

class ProductService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def list_products(self, limit: int = 20, cursor: Optional[str] = None) -> tuple[List[ProductListItemDTO], str | None]:
        async with self.uow as uow:
            products = await uow.products.list_products(limit=limit, cursor=cursor)
            
            # Convert to DTO
            dtos = []
            for p in products:
                dtos.append(ProductListItemDTO(
                    id=p.id,
                    name=p.name,
                    thumbnail_url=p.thumbnail_url,
                    price=MoneyDTO(amount=p.price_amount, currency=p.price_currency),
                    stock=p.stock,
                    nearest_delivery_date=p.nearest_delivery_date
                ))
            
            # Simple cursor logic for infinite scroll
            next_cursor = products[-1].id if len(products) == limit else None
            
            return dtos, next_cursor

    async def get_product_details(self, product_id: str, offers_sort: str = "price") -> Optional[ProductDetailsDTO]:
        async with self.uow as uow:
            product = await uow.products.get_by_id(product_id)
            if not product:
                return None
                
            offers = product.offers
            # Sort offers
            if offers_sort == "price":
                offers.sort(key=lambda o: o.price_amount)
            elif offers_sort == "delivery_date":
                offers.sort(key=lambda o: o.delivery_date)
                
            offer_dtos = []
            for o in offers:
                seller_dto = SellerDTO(id=o.seller.id, name=o.seller.name, rating=o.seller.rating) if o.seller else None
                offer_dtos.append(OfferWithSellerDTO(
                    id=o.id,
                    product_id=o.product_id,
                    seller_id=o.seller_id,
                    price=MoneyDTO(amount=o.price_amount, currency=o.price_currency),
                    delivery_date=o.delivery_date,
                    seller=seller_dto
                ))
                
            attribute_dtos = [ProductAttributeDTO(key=attr.get("key", ""), value=attr.get("value", "")) for attr in product.attributes]
            
            return ProductDetailsDTO(
                id=product.id,
                name=product.name,
                image_url=product.image_url,
                attributes=attribute_dtos,
                offers=offer_dtos
            )

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

    async def update_image(self, product_id: str, image_url: str, thumbnail_url: str) -> Optional[Product]:
        async with self.uow as uow:
            product = await uow.products.get_by_id(product_id)
            if not product:
                return None
            product.image_url = image_url
            product.thumbnail_url = thumbnail_url
            await uow.products.update(product)
            await uow.commit()
            return product
