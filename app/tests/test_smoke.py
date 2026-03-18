import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_list_products_public():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/v1/public/products")
    # Even if DB is empty, should return 200 OK and "items" list
    assert response.status_code == 200
    assert "items" in response.json()

@pytest.mark.asyncio
async def test_admin_login_failure():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/v1/admin/auth/login", data={"username": "wrong", "password": "var"})
    assert response.status_code == 401
