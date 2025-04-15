from typing import Optional

from pydantic import BaseModel

from app.schemas.address import AddressCreate, AddressResponse
from app.schemas.user import UserCreate, UserResponse

class ONGBase(BaseModel):
    description: Optional[str] = None


class ONGCreate(ONGBase):
    address: AddressCreate
    user: UserCreate

class ONGResponse(ONGBase):
    id: int
    user_id: int
    description: Optional[str] = None
    address: AddressResponse
    user: UserResponse

    class Config:
        from_attributes = True