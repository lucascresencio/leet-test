from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, DateTime, UniqueConstraint, Date
from sqlalchemy.orm import relationship
from app.config.database import Base
from datetime import datetime

class Volunteer(Base):
    __tablename__ = "volunteers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    photo = Column(String)
    address_id = Column(Integer, ForeignKey("address.id"), nullable=True)
    birthdate = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    address = relationship("Address")
    projects = relationship("ProjectVolunteer", back_populates="volunteer")
    bases = relationship("BaseVolunteer", back_populates="volunteer")