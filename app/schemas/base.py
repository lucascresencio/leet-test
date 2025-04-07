from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import date, datetime
from app.schemas.address import AddressCreate, AddressResponse

class BaseCreate(BaseModel):
    ong_id: int
    address: AddressCreate
    name: str
    foundation_date: date
    email: Optional[str] = None
    phone_number: Optional[str] = None
    main_photo: Optional[str] = None
    photo_urls: Optional[List[str]] = []
    volunteer_ids: Optional[List[int]] = []
    notes: Optional[str] = None

class BaseUpdate(BaseModel):
    name: Optional[str] = None
    foundation_date: Optional[date] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    main_photo: Optional[str] = None
    notes: Optional[str] = None

class BaseResponse(BaseModel):
    id: int
    ong_id: int
    address_id: int
    name: str
    foundation_date: date
    email: Optional[str] = None
    phone_number: Optional[str] = None
    main_photo: Optional[str] = None
    notes: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    address: AddressResponse
    photos: List["BasePhotoResponse"] = []
    volunteers: List["BaseVolunteerResponse"] = []

    class Config:
        from_attributes = True

class BasePhotoCreate(BaseModel):
    photo_url: str

class BasePhotoResponse(BaseModel):
    id: int
    base_id: int
    photo_url: str
    uploaded_at: datetime

    class Config:
        from_attributes = True

class BaseVolunteerResponse(BaseModel):
    id: int
    base_id: int
    volunteer_id: int
    volunteer_name: str
    joined_at: datetime

    class Config:
        from_attributes = True