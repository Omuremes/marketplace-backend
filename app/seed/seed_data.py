import asyncio
import random
from datetime import datetime, timedelta
from app.infrastructure.db.session import AsyncSessionLocal
from app.infrastructure.db.uow import SqlAlchemyUnitOfWork
from app.domain.entities.product import Product
from app.domain.entities.seller import Seller
from app.domain.entities.offer import Offer

async def seed_database():
    uow = SqlAlchemyUnitOfWork(session_factory=AsyncSessionLocal)
    async with uow:
        # Check if already seeded
        existing_products = await uow.products.list_products(limit=1)
        if existing_products:
            print("Database already seeded")
            return

        print("Seeding Sellers...")
        sellers = []
        for i in range(10):
            seller = Seller.create(name=f"Seller {i+1}", rating=round(random.uniform(3.0, 5.0), 1))
            await uow.sellers.add(seller)
            sellers.append(seller)

        print("Seeding Products and Offers...")
        colors = ["Red", "Blue", "Green", "Black", "White"]
        materials = ["Plastic", "Metal", "Wood", "Glass"]
        
        for i in range(110):  # 110 products
            attributes = [
                {"key": "Color", "value": random.choice(colors)},
                {"key": "Material", "value": random.choice(materials)}
            ]
            product = Product.create(
                name=f"Product {i+1}",
                price_amount=round(random.uniform(10.0, 1000.0), 2),
                price_currency="USD",
                stock=random.randint(0, 100),
                attributes=attributes
            )
            # Default placeholder image
            product.image_url = "https://via.placeholder.com/600"
            product.thumbnail_url = "https://via.placeholder.com/150"
            await uow.products.add(product)

            # 2 to 6 offers per product
            num_offers = random.randint(2, 6)
            sampled_sellers = random.sample(sellers, num_offers)
            for seller in sampled_sellers:
                # Delivery date this week
                days_ahead = random.randint(1, 7)
                delivery_date = (datetime.now() + timedelta(days=days_ahead)).date()
                offer = Offer.create(
                    product_id=product.id,
                    seller_id=seller.id,
                    price_amount=round(product.price_amount * random.uniform(0.9, 1.2), 2),
                    price_currency="USD",
                    delivery_date=delivery_date
                )
                await uow.offers.add(offer)

        await uow.commit()
        print("Database seeded successfully with 110 products, 10 sellers, and multiple offers.")

if __name__ == "__main__":
    asyncio.run(seed_database())
