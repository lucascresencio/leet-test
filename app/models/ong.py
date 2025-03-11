from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base


class ONG(Base):
    __tablename__ = "ongs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    cnpj = Column(String, unique=True)
    address_id = Column(Integer, ForeignKey("address.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship definition
    address = relationship("Address")
    user = relationship("User")