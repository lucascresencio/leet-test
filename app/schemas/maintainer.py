from typing import Optional

from pydantic import BaseModel

from app.schemas.address import AddressCreate, AddressResponse
from app.schemas.user import UserCreate, UserResponse

class MaintainerBase(BaseModel):
    is_business: bool


class MaintainerCreate(MaintainerBase):
    address: AddressCreate
    user: UserCreate
    ong_id: int
    is_business: Optional[bool] = False

class MaintainerResponse(MaintainerBase):
    id: int
    address: AddressResponse
    user: UserResponse
    ong_id: Optional[int]
    is_business: Optional[bool] = False
    client_id: Optional[str] = None

    class Config:
        from_attributes = True