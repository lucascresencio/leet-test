from typing import Optional

from pydantic import BaseModel, EmailStr, validator


class UserBase(BaseModel):
    username: str
    name: str
    email: Optional[EmailStr] = None
    document: Optional[str] = None
    phone_number: Optional[str] = None
    user_type: str


class UserCreate(UserBase):
    username: str
    name: str
    password: str
    user_type: str
    photo: Optional[str] = None

    @validator("phone_number")
    def validate_phone_number(cls, value):
        import re
        # Remove caracteres não numéricos
        cleaned = re.sub(r'\D', '', value)
        # Adiciona +55 se não tiver código de país
        if not cleaned.startswith('+'):
            if cleaned.startswith('55'):
                cleaned = f'+{cleaned}'
            else:
                cleaned = f'+55{cleaned}'
        # Valida o padrão da Pagar.me
        if not re.match(r'^\+(?:[0-9] ?){6,14}[0-9]$', cleaned):
            raise ValueError("Phone number must be in international format (e.g., +5511999999999)")
        return value

class UserResponse(BaseModel):
    id: int
    username: str
    name: Optional[str] = None
    document: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    status: Optional[str] = None
    user_type: Optional[str] = None
    photo: Optional[str] = None

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    document: Optional[str] = None
    phone_number: Optional[str] = None

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    username: str
    name: Optional[str] = None
    document: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    user_type: Optional[str] = None
    role: Optional[str] = None
    photo: Optional[str] = None
