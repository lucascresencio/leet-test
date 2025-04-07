from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.address import AddressCreate, AddressResponse

class AttendeeCreate(BaseModel):
    name: str
    document: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: AddressCreate

class AttendeeUpdate(BaseModel):
    name: Optional[str] = None
    document: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None

class AttendeeResponse(BaseModel):
    id: int
    name: str
    document: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address_id: Optional[int] = None
    address: Optional[AddressResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True