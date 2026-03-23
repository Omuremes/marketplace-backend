from app.domain.entities.product import Product
from app.domain.entities.seller import Seller
from app.domain.entities.offer import Offer
from app.infrastructure.db.models import ProductModel, SellerModel, OfferModel, ProductAttributeModel, AdminModel
from app.domain.entities.admin import Admin

class DomainMapper:
    @staticmethod
    def to_product_domain(model: ProductModel) -> Product:
        offers = [DomainMapper.to_offer_domain(offer) for offer in getattr(model, "offers", [])]
        
        nearest_delivery_date = None
        if offers:
            nearest_delivery_date = min((offer.delivery_date for offer in offers), default=None)

        attributes = [{"key": a.key, "value": a.value} for a in getattr(model, "attributes", [])]

        return Product(
            id=model.id,
            name=model.name,
            price_amount=float(model.price_amount),
            price_currency=model.price_currency,
            stock=model.stock,
            image_object_key=model.image_object_key,
            thumbnail_object_key=model.thumbnail_object_key,
            attributes=attributes,
            offers=offers,
            nearest_delivery_date=nearest_delivery_date
        )

    @staticmethod
    def to_seller_domain(model: SellerModel) -> Seller:
        return Seller(
            id=model.id,
            name=model.name,
            email=model.email,
            password_hash=model.password_hash,
            rating=float(model.rating)
        )

    @staticmethod
    def to_admin_domain(model: AdminModel) -> Admin:
        return Admin(
            id=model.id,
            email=model.email,
            password_hash=model.password_hash
        )

    @staticmethod
    def to_offer_domain(model: OfferModel) -> Offer:
        seller = DomainMapper.to_seller_domain(model.seller) if getattr(model, "seller", None) else None
        return Offer(
            id=model.id,
            product_id=model.product_id,
            seller_id=model.seller_id,
            price_amount=float(model.price_amount),
            price_currency=model.price_currency,
            delivery_date=model.delivery_date,
            seller=seller
        )

    @staticmethod
    def to_product_model(domain: Product) -> ProductModel:
        attr_models = [ProductAttributeModel(product_id=domain.id, key=a["key"], value=a["value"]) for a in domain.attributes]
        return ProductModel(
            id=domain.id,
            name=domain.name,
            price_amount=domain.price_amount,
            price_currency=domain.price_currency,
            stock=domain.stock,
            image_object_key=domain.image_object_key,
            thumbnail_object_key=domain.thumbnail_object_key,
            attributes=attr_models
        )

    @staticmethod
    def to_seller_model(domain: Seller) -> SellerModel:
        return SellerModel(
            id=domain.id,
            name=domain.name,
            email=domain.email,
            password_hash=domain.password_hash,
            rating=domain.rating
        )

    @staticmethod
    def to_admin_model(domain: Admin) -> AdminModel:
        return AdminModel(
            id=domain.id,
            email=domain.email,
            password_hash=domain.password_hash
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
