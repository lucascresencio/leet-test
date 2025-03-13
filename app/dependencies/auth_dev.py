from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from datetime import timedelta
from pydantic import BaseModel
import os
from app.services.auth_service import create_access_token

load_dotenv()

router = APIRouter(prefix="/developer", tags=["developer"])

# Chave secreta para desenvolvedor (mantenha segura, pode ser movida para .env)
DEVELOPER_SECRET = os.getenv("DEVELOPER_SECRET")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Schema para requisição de token de desenvolvedor
class DeveloperTokenRequest(BaseModel):
    secret: str

class DeveloperTokenResponse(BaseModel):
    access_token: str
    token_type: str


# Endpoint para gerar token de desenvolvedor
@router.post("/token", response_model=DeveloperTokenResponse)
def get_developer_token(request: DeveloperTokenRequest):
    if request.secret != DEVELOPER_SECRET:
        raise HTTPException(status_code=403, detail="Invalid developer secret")

    # Gera um token com permissões de admin
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": "developer", "type": "staff", "role": "admin"},
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }