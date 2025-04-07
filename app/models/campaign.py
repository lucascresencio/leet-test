from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, DateTime, Numeric
from sqlalchemy.orm import relationship
from app.config.database import Base as SQLAlchemyBase
from datetime import datetime

class Campaign(SQLAlchemyBase):
    __tablename__ = "campaigns"
    id = Column(Integer, primary_key=True, index=True)
    base_id = Column(Integer, ForeignKey("bases.id"), nullable=True)
    ong_id = Column(Integer, ForeignKey("ongs.id"), nullable=False)
    main_photo = Column(String)
    title = Column(String, nullable=False)
    description = Column(String)
    goal = Column(Numeric(15, 2), nullable=False)  # Decimal com precisão 15, escala 2
    status = Column(String(1), nullable=False, default="I")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("status IN ('I', 'A', 'E')", name="check_status"),
    )

    base = relationship("Base", back_populates="campaigns")
    ong = relationship("ONG", back_populates="campaigns")
    photos = relationship("CampaignPhoto", back_populates="campaign")

class CampaignPhoto(SQLAlchemyBase):
    __tablename__ = "campaign_photos"
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    photo_url = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    campaign = relationship("Campaign", back_populates="photos")