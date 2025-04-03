from pydantic import BaseModel

from app.schemas.address import AddressCreate, AddressResponse
from app.schemas.user import UserCreate, UserResponse

class StaffBase(BaseModel):
    email: str
    name: str
    role: str  # "admin", "office", "volunteer"

class StaffCreate(StaffBase):
    name: str
    ong_id: int
    address: AddressCreate
    user: UserCreate

    class Config:
        schema_extra = {
            "example": {
                "name": "João Silva",
                "email": "joao@ong.com",
                "ong_id": 1,
                "address": {
                    "street": "Rua das Flores",
                    "city": "São Paulo",
                    "state": "SP",
                    "zip_code": "01000-000"
                },
                "user": {
                    "username": "joao123",
                    "password": "senha123",
                    "user_type": "staff"
                },
                "role": "admin"
            }
        }

class StaffResponse(StaffBase):
    id: int
    user_id: int
    name: str
    role: str  # Retorna o nome do papel (ex.: "admin")
    ong_id: int
    address_id: int
    user: UserResponse
    address: AddressResponse

    class Config:
        from_attributes = True
    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            user_id=obj.user_id,
            name=obj.name,
            email=obj.email,
            role=obj.role.name if obj.role else None,
            ong_id=obj.ong_id,
            address_id=obj.address_id,
            user=UserResponse.from_orm(obj.user),
            address=AddressResponse.from_orm(obj.address)
        )