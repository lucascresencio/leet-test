from pydantic import BaseModel

from app.schemas.address import AddressCreate, AddressResponse
from app.schemas.user import UserCreate, UserResponse

class ONGBase(BaseModel):
    name: str
    cnpj: str


class ONGCreate(ONGBase):
    address: AddressCreate
    user: UserCreate

class ONGResponse(ONGBase):
    id: int
    address: AddressResponse
    user: UserResponse

    class Config:
        from_attributes = True