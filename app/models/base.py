from sqlalchemy import Column, Integer, String, ForeignKey, Date, CheckConstraint, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from app.config.database import Base as SQLAlchemyBase
from datetime import datetime

class Base(SQLAlchemyBase):
    __tablename__ = "bases"
    id = Column(Integer, primary_key=True, index=True)
    ong_id = Column(Integer, ForeignKey("ongs.id"), nullable=False)
    address_id = Column(Integer, ForeignKey("address.id"), nullable=False)
    name = Column(String, nullable=False)
    foundation_date = Column(Date, nullable=False)
    email = Column(String(255))
    phone_number = Column(String(20))
    main_photo = Column(String)
    notes = Column(String)
    status = Column(String(1), nullable=False, default="I")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("status IN ('I', 'A', 'E')", name="check_status"),
    )

    ong = relationship("ONG", back_populates="bases")
    address = relationship("Address")
    photos = relationship("BasePhoto", back_populates="base")
    volunteers = relationship("BaseVolunteer", back_populates="base")
    campaigns = relationship("Campaign", back_populates="base")

class BasePhoto(SQLAlchemyBase):
    __tablename__ = "base_photos"
    id = Column(Integer, primary_key=True, index=True)
    base_id = Column(Integer, ForeignKey("bases.id"), nullable=False)
    photo_url = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    base = relationship("Base", back_populates="photos")

class BaseVolunteer(SQLAlchemyBase):
    __tablename__ = "base_volunteers"
    id = Column(Integer, primary_key=True, index=True)
    base_id = Column(Integer, ForeignKey("bases.id"), nullable=False)
    volunteer_id = Column(Integer, ForeignKey("volunteers.id"), nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint("base_id", "volunteer_id", name="unique_base_volunteer"),)

    base = relationship("Base", back_populates="volunteers")
    volunteer = relationship("Volunteer", back_populates="bases")