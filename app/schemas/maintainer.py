from typing import Optional

from pydantic import BaseModel

from app.schemas.address import AddressCreate, AddressResponse
from app.schemas.user import UserCreate, UserResponse

class MaintainerBase(BaseModel):
    is_business: bool


class MaintainerCreate(MaintainerBase):
    address: AddressCreate
    user: UserCreate
    is_business: Optional[bool] = False

class MaintainerResponse(MaintainerBase):
    id: int
    address: AddressResponse
    user: UserResponse
    is_business: Optional[bool] = False

    class Config:
        from_attributes = True