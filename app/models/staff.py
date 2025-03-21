from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from typing_extensions import Optional

from app.config.database import Base


class Staff(Base):
    __tablename__ = "staff"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    name = Column(String)
    email = Column(String, unique=True, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    ong_id = Column(Integer, ForeignKey("ongs.id"), nullable=True)
    address_id = Column(Integer, ForeignKey("address.id"), nullable=True)

    # relationships
    user = relationship("User")
    role = relationship("Role")
    ong = relationship("ONG")
    address = relationship("Address")
