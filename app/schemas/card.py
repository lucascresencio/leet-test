from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CardCreate(BaseModel):
    number: str
    holder_name: str
    expiration_date: str  # Formato MMAA (ex.: 1225)
    cvv: str

class CardResponse(BaseModel):
    id: int
    maintainer_id: int
    card_id: str  # ID do cartão na Pagar.me
    last_four_digits: str
    brand: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True