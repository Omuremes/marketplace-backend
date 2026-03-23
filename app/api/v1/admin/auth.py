from fastapi import APIRouter, HTTPException, Depends
from app.application.services.auth_service import AuthService
from pydantic import BaseModel
from app.api.deps import get_uow
from app.application.uow import UnitOfWork

router = APIRouter()

class AdminLoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
async def login(body: AdminLoginRequest, uow: UnitOfWork = Depends(get_uow)):
    """Admin login — accepts application/json as per OpenAPI spec."""
    is_authenticated = await AuthService.authenticate_admin(uow, body.username, body.password)
    if not is_authenticated:
        raise HTTPException(
            status_code=401,
            detail={"error": "unauthorized", "message": "Incorrect username or password"}
        )
    access_token = AuthService.create_access_token(data={"sub": body.username, "role": "admin"})
    refresh_token = AuthService.create_refresh_token(data={"sub": body.username, "role": "admin"})
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

