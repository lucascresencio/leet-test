from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.schemas.address import AddressCreate, AddressResponse

class VolunteerCreate(BaseModel):
    name: str
    photo: Optional[str] = None
    address: AddressCreate
    birthdate: date

class VolunteerUpdate(BaseModel):
    name: Optional[str] = None
    photo: Optional[str] = None
    birthdate: Optional[date] = None

class VolunteerResponse(BaseModel):
    id: int
    name: str
    photo: Optional[str] = None
    address_id: int
    address: AddressResponse
    birthdate: date
    created_at: datetime

    class Config:
        from_attributes = True