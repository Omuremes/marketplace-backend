from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.application.services.auth_service import AuthService
from pydantic import BaseModel

router = APIRouter()

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not AuthService.authenticate_admin(form_data.username, form_data.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = AuthService.create_access_token(data={"sub": form_data.username})
    return TokenResponse(access_token=access_token)
