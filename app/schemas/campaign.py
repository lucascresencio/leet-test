from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

class CampaignCreate(BaseModel):
    base_id: Optional[int] = None  # Opcional
    ong_id: int  # Obrigatório
    main_photo: Optional[str] = None
    title: str
    description: Optional[str] = None
    goal: Decimal
    photo_urls: Optional[List[str]] = []

class CampaignUpdate(BaseModel):
    base_id: Optional[int] = None
    main_photo: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    goal: Optional[Decimal] = None

class CampaignResponse(BaseModel):
    id: int
    base_id: Optional[int] = None
    ong_id: int
    main_photo: Optional[str] = None
    title: str
    description: Optional[str] = None
    goal: Decimal
    status: str
    created_at: datetime
    updated_at: datetime
    photos: List["CampaignPhotoResponse"] = []

    class Config:
        from_attributes = True

class CampaignPhotoResponse(BaseModel):
    id: int
    campaign_id: int
    photo_url: str
    uploaded_at: datetime

    class Config:
        from_attributes = True