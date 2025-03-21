from pydantic import BaseModel

from app.schemas.address import AddressCreate, AddressResponse
from app.schemas.user import UserCreate, UserResponse

class MaintainerBase(BaseModel):
    name: str
    is_business: bool


class MaintainerCreate(MaintainerBase):
    address: AddressCreate
    user: UserCreate

class MaintainerResponse(MaintainerBase):
    id: int
    address: AddressResponse
    user: UserResponse

    class Config:
        from_attributes = True