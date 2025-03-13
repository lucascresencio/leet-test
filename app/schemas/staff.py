from pydantic import BaseModel

from app.schemas.address import AddressCreate, AddressResponse
from app.schemas.user import UserCreate, UserResponse

class StaffBase(BaseModel):
    email: str
    role: str  # "admin", "office", "volunteer"

class StaffCreate(StaffBase):
    pass

class StaffResponse(StaffBase):
    id: int
    user_id: int
    role: str  # Retorna o nome do papel (ex.: "admin")

    class Config:
        from_attributes = True
    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            user_id=obj.user_id,
            email=obj.email,
            role=obj.role.name if obj.role else None
        )