from typing import Optional

from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
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

class UserResponse(BaseModel):
    id: int
    username: str
    name: Optional[str] = None
    document: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    status: str
    user_type: str
    photo: Optional[str] = None

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None
    document: Optional[str] = None
    phone_number: Optional[str] = None

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    username: str
    name: str
    document: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    user_type: str
    role: Optional[str] = None
    photo: Optional[str] = None
