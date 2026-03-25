from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.config.settings import settings

from app.api.v1.public.products import router as public_products_router
from app.api.v1.admin.auth import router as admin_auth_router
from app.api.v1.admin.products import router as admin_products_router
from app.api.v1.admin.offers import router as admin_offers_router
from app.api.v1.public.sellers import router as public_sellers_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(public_products_router, prefix=f"{settings.API_V1_STR}/public/products", tags=["Public"])
app.include_router(public_sellers_router, prefix=f"{settings.API_V1_STR}/public/sellers", tags=["PublicSellers"])

# Admin
app.include_router(admin_auth_router, prefix=f"{settings.API_V1_STR}/admin/auth", tags=["AdminAuth"])
app.include_router(admin_products_router, prefix=f"{settings.API_V1_STR}/admin/products", tags=["AdminProducts"])
app.include_router(admin_offers_router, prefix=f"{settings.API_V1_STR}/admin", tags=["AdminOffers"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
