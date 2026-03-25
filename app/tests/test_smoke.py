from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_list_products_public():
    response = client.get("/v1/public/products")
    # Even if DB is empty, should return 200 OK and "items" list
    assert response.status_code == 200
    assert "items" in response.json()


