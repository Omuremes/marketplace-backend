from dataclasses import dataclass
from typing import Optional

import pytest
from app.application.services.product_service import ProductService
from app.domain.entities.product import Product


@dataclass
class _FakeStorageClient:
    def get_file_url(self, object_key: str) -> str:
        return f"https://files.local/{object_key}"


class _FakeProductRepo:
    def __init__(self, products: list[Product]):
        self._products = products
        self.last_call: dict = {}

    async def list_products(
        self,
        limit: int,
        cursor: Optional[str] = None,
        search: Optional[str] = None,
    ) -> list[Product]:
        self.last_call = {"limit": limit, "cursor": cursor, "search": search}

        filtered = self._products
        if search:
            search_lower = search.lower()
            filtered = [p for p in filtered if search_lower in p.name.lower()]

        if cursor:
            filtered = [p for p in filtered if p.id > cursor]

        filtered = sorted(filtered, key=lambda p: p.id)
        return filtered[:limit]


class _FakeUoW:
    def __init__(self, products_repo: _FakeProductRepo):
        self.products = products_repo

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return None


@pytest.mark.asyncio
async def test_product_service_search_and_cursor_pagination():
    products = [
        Product(id="a", name="Laptop 1", price_amount=100, price_currency="USD", stock=1),
        Product(id="b", name="Laptop 2", price_amount=200, price_currency="USD", stock=2),
        Product(id="c", name="Laptop 3", price_amount=300, price_currency="USD", stock=3),
        Product(id="d", name="Phone 1", price_amount=400, price_currency="USD", stock=4),
    ]

    repo = _FakeProductRepo(products)
    service = ProductService(uow=_FakeUoW(repo))
    service.storage_client = _FakeStorageClient()

    items, next_cursor = await service.list_products(limit=2, search="laptop")

    assert repo.last_call == {"limit": 3, "cursor": None, "search": "laptop"}
    assert [item.id for item in items] == ["a", "b"]
    assert next_cursor == "b"

    items_page_2, next_cursor_page_2 = await service.list_products(limit=2, cursor="b", search="laptop")

    assert repo.last_call == {"limit": 3, "cursor": "b", "search": "laptop"}
    assert [item.id for item in items_page_2] == ["c"]
    assert next_cursor_page_2 is None

