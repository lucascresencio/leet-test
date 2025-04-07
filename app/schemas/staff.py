from pydantic import BaseModel

from app.schemas.address import AddressCreate, AddressResponse
from app.schemas.user import UserCreate, UserResponse

class StaffBase(BaseModel):
    role: str  # "admin", "office"

class StaffCreate(StaffBase):
    ong_id: int
    address: AddressCreate
    user: UserCreate

    class Config:
        schema_extra = {
            "example": {
                "name": "João Silva",
                "ong_id": 1,
                "address": {
                    "street": "Rua das Flores",
                    "city": "São Paulo",
                    "state": "SP",
                    "zip_code": "01000-000"
                },
                "user": {
                    "username": "joao123",
                    "email": "joao@ong.com",
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
            role=obj.role.name if obj.role else None,
            ong_id=obj.ong_id,
            address_id=obj.address_id,
            user=UserResponse.from_orm(obj.user),
            address=AddressResponse.from_orm(obj.address)
        )