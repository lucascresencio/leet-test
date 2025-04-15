from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.config.database import Base
import enum
from datetime import datetime


class PaymentMethod(enum.Enum):
    CREDIT_CARD = "credit_card"
    BOLETO = "boleto"
    PIX = "pix"


class TransactionStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    CANCELED = "canceled"
    EXPIRED = "expired"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    maintainer_id = Column(Integer, ForeignKey("maintainers.id"), nullable=False)
    ong_id = Column(Integer, ForeignKey("ongs.id"), nullable=False)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)
    base_id = Column(Integer, ForeignKey("bases.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    attendee_id = Column(Integer, ForeignKey("attendees.id"), nullable=True)
    amount = Column(Float, nullable=False)
    commission_amount = Column(Float, nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    status = Column(Enum(TransactionStatus), nullable=False, default=TransactionStatus.PENDING)
    order_id = Column(String, nullable=True)
    charge_id = Column(String, nullable=True)
    card_id = Column(String, nullable=True)
    boleto_url = Column(String, nullable=True)
    boleto_barcode = Column(String, nullable=True)
    pix_qr_code = Column(String, nullable=True)
    pix_code = Column(String, nullable=True)
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    maintainer = relationship("Maintainer", back_populates="transactions")
    ong = relationship("ONG")
    campaign = relationship("Campaign")
    base = relationship("Base")
    project = relationship("Project")
    attendee = relationship("Attendee")