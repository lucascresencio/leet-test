from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from app.schemas.address import AddressCreate, AddressResponse
from app.schemas.user import UserResponse

class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    target_audience: str
    address: AddressCreate
    ong_id: int
    responsible_staff_id: Optional[int] = None
    main_photo: Optional[str] = None
    photo_urls: Optional[List[str]] = []
    attendee_ids: Optional[List[int]] = []
    volunteer_ids: Optional[List[int]] = []

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_audience: Optional[str] = None
    responsible_staff_id: Optional[int] = None
    main_photo: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    ong_id: int
    address_id: int
    title: str
    description: Optional[str] = None
    target_audience: str
    main_photo: Optional[str] = None
    responsible_staff: Optional[UserResponse] = None
    status: str
    created_at: datetime
    updated_at: datetime
    photos: List["ProjectPhotoResponse"] = []
    attendees: List["ProjectAttendeeResponse"] = []
    volunteers: List["ProjectVolunteerResponse"] = []

    class Config:
        from_attributes = True

class ProjectPhotoCreate(BaseModel):
    photo_url: str

class ProjectPhotoResponse(BaseModel):
    id: int
    project_id: int
    photo_url: str
    uploaded_at: datetime

    class Config:
        from_attributes = True

class ProjectAttendeeResponse(BaseModel):
    id: int
    project_id: int
    attendee_id: int
    attendee_name: str
    added_at: datetime

    class Config:
        from_attributes = True

class ProjectVolunteerResponse(BaseModel):
    id: int
    project_id: int
    volunteer_id: int
    volunteer_name: str
    joined_at: datetime

    class Config:
        from_attributes = True