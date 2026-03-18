from app.domain.entities.product import Product
from app.domain.entities.seller import Seller
from app.domain.entities.offer import Offer
from app.infrastructure.db.models import ProductModel, SellerModel, OfferModel

class DomainMapper:
    @staticmethod
    def to_product_domain(model: ProductModel) -> Product:
        offers = [DomainMapper.to_offer_domain(offer) for offer in getattr(model, "offers", [])]
        
        # Calculate nearest delivery date from offers
        nearest_delivery_date = None
        if offers:
            nearest_delivery_date = min((offer.delivery_date for offer in offers), default=None)

        return Product(
            id=model.id,
            name=model.name,
            price_amount=model.price_amount,
            price_currency=model.price_currency,
            stock=model.stock,
            image_url=model.image_url,
            thumbnail_url=model.thumbnail_url,
            attributes=model.attributes,
            offers=offers,
            nearest_delivery_date=nearest_delivery_date
        )

    @staticmethod
    def to_seller_domain(model: SellerModel) -> Seller:
        return Seller(
            id=model.id,
            name=model.name,
            rating=model.rating
        )

    @staticmethod
    def to_offer_domain(model: OfferModel) -> Offer:
        seller = DomainMapper.to_seller_domain(model.seller) if getattr(model, "seller", None) else None
        return Offer(
            id=model.id,
            product_id=model.product_id,
            seller_id=model.seller_id,
            price_amount=model.price_amount,
            price_currency=model.price_currency,
            delivery_date=model.delivery_date,
            seller=seller
        )

    @staticmethod
    def to_product_model(domain: Product) -> ProductModel:
        return ProductModel(
            id=domain.id,
            name=domain.name,
            price_amount=domain.price_amount,
            price_currency=domain.price_currency,
            stock=domain.stock,
            image_url=domain.image_url,
            thumbnail_url=domain.thumbnail_url,
            attributes=domain.attributes
        )

    @staticmethod
    def to_seller_model(domain: Seller) -> SellerModel:
        return SellerModel(
            id=domain.id,
            name=domain.name,
            rating=domain.rating
        )

    @staticmethod
    def to_offer_model(domain: Offer) -> OfferModel:
        return OfferModel(
            id=domain.id,
            product_id=domain.product_id,
            seller_id=domain.seller_id,
            price_amount=domain.price_amount,
            price_currency=domain.price_currency,
            delivery_date=domain.delivery_date
        )
