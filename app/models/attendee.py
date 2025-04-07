from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, DateTime, UniqueConstraint, Date
from sqlalchemy.orm import relationship
from app.config.database import Base
from datetime import datetime

class Attendee(Base):
    __tablename__ = "attendees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    document = Column(String(50), unique=True)
    address_id = Column(Integer, ForeignKey("address.id"), nullable=True)
    email = Column(String(255))
    phone_number = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)

    address = relationship("Address")
    projects = relationship("ProjectAttendee", back_populates="attendee")