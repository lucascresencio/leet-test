from typing import Optional

from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    document: Optional[str] = None
    phone_number: Optional[str] = None
    user_type: str


class UserCreate(UserBase):
    password: str
    user_type: str

class UserResponse(UserBase):
    id: int
    user_type: str

    class Config:
        orm_mode = True
        from_attributes = True

    # Map user_type.name to user_type
    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            username=obj.username,
            user_type=obj.user_type.name if obj.user_type else None
        )

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
    document: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    user_type: str
    role: Optional[str] = None