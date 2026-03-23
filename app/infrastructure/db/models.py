from sqlalchemy import String, Integer, ForeignKey, Date, Numeric, DateTime, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from datetime import date, datetime
import uuid
from .session import Base

class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(Text, nullable=False)
    price_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    price_currency: Mapped[str] = mapped_column(Text, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    image_object_key: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    thumbnail_object_key: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("now()"), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("now()"), onupdate=text("now()"), nullable=False)
    
    attributes: Mapped[List["ProductAttributeModel"]] = relationship("ProductAttributeModel", back_populates="product", cascade="all, delete-orphan")
    offers: Mapped[List["OfferModel"]] = relationship("OfferModel", back_populates="product", cascade="all, delete-orphan")

class ProductAttributeModel(Base):
    __tablename__ = "product_attributes"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    key: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)

    product: Mapped["ProductModel"] = relationship("ProductModel", back_populates="attributes")

class AdminModel(Base):
    __tablename__ = "admins"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)

class SellerModel(Base):
    __tablename__ = "sellers"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    rating: Mapped[float] = mapped_column(Numeric(3, 2), nullable=False)

    offers: Mapped[List["OfferModel"]] = relationship("OfferModel", back_populates="seller", cascade="all, delete-orphan")

class OfferModel(Base):
    __tablename__ = "offers"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    seller_id: Mapped[str] = mapped_column(ForeignKey("sellers.id", ondelete="CASCADE"), nullable=False, index=True)
    price_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    price_currency: Mapped[str] = mapped_column(Text, nullable=False)
    delivery_date: Mapped[date] = mapped_column(Date, nullable=False)

    product: Mapped["ProductModel"] = relationship("ProductModel", back_populates="offers")
    seller: Mapped["SellerModel"] = relationship("SellerModel", back_populates="offers")
