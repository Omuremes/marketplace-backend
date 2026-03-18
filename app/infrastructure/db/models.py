from sqlalchemy import String, Float, Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from typing import List, Optional, Any
from datetime import date
from .session import Base

class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    price_amount: Mapped[float] = mapped_column(Float, nullable=False)
    price_currency: Mapped[str] = mapped_column(String, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    image_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    thumbnail_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    attributes: Mapped[List[dict[str, Any]]] = mapped_column(JSONB, nullable=False, default=list)

    offers: Mapped[List["OfferModel"]] = relationship("OfferModel", back_populates="product", cascade="all, delete-orphan")


class SellerModel(Base):
    __tablename__ = "sellers"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    offers: Mapped[List["OfferModel"]] = relationship("OfferModel", back_populates="seller", cascade="all, delete-orphan")


class OfferModel(Base):
    __tablename__ = "offers"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    seller_id: Mapped[str] = mapped_column(ForeignKey("sellers.id", ondelete="CASCADE"), nullable=False, index=True)
    price_amount: Mapped[float] = mapped_column(Float, nullable=False)
    price_currency: Mapped[str] = mapped_column(String, nullable=False)
    delivery_date: Mapped[date] = mapped_column(Date, nullable=False)

    product: Mapped["ProductModel"] = relationship("ProductModel", back_populates="offers")
    seller: Mapped["SellerModel"] = relationship("SellerModel", back_populates="offers")
