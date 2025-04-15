from typing import Optional

from pydantic import BaseModel

from app.schemas.address import AddressCreate, AddressResponse
from app.schemas.role import RoleResponse
from app.schemas.user import UserCreate, UserResponse

class StaffBase(BaseModel):
    role_id: str  # "admin", "office"

class StaffCreate(StaffBase):
    ong_id: Optional[int] = None
    address: AddressCreate
    user: UserCreate
    role_id: str

class StaffResponse(BaseModel):
    id: int
    user_id: int
    ong_id: int
    role_id: str  # Obrigatório
    role: RoleResponse  # Obrigatório
    address_id: Optional[int] = None  # Opcional
    address: Optional[AddressResponse] = None  # Opcional
    user: UserResponse

    class Config:
        from_attributes = True