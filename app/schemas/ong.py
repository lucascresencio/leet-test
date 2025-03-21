from typing import Optional

from pydantic import BaseModel

from app.schemas.address import AddressCreate, AddressResponse
from app.schemas.user import UserCreate, UserResponse

class ONGBase(BaseModel):
    name: str
    document: Optional[str] = None


class ONGCreate(ONGBase):
    address: AddressCreate
    user: UserCreate

class ONGResponse(ONGBase):
    id: int
    document: Optional[str] = None
    address: AddressResponse
    user: UserResponse

    class Config:
        from_attributes = True