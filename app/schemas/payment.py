from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class CardDetails(BaseModel):
    card_id: Optional[str] = None
    number: Optional[str] = None
    holder_name: Optional[str] = None
    expiration_date: Optional[str] = None
    cvv: Optional[str] = None

class PaymentRequest(BaseModel):
    amount: float
    payment_method: Literal["credit_card", "boleto", "pix"]
    card_details: Optional[CardDetails] = None
    ong_id: int
    campaign_id: Optional[int] = None
    base_id: Optional[int] = None
    project_id: Optional[int] = None
    attendee_id: Optional[int] = None

class PaymentResponse(BaseModel):
    transaction_id: int
    amount: float
    commission_amount: float
    payment_method: str
    status: str
    ong_id: int
    campaign_id: Optional[int] = None
    base_id: Optional[int] = None
    project_id: Optional[int] = None
    attendee_id: Optional[int] = None
    order_id: Optional[str] = None
    charge_id: Optional[str] = None
    card_id: Optional[str] = None
    boleto_url: Optional[str] = None
    boleto_barcode: Optional[str] = None
    pix_qr_code: Optional[str] = None
    pix_code: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True