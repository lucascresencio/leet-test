from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.config.database import Base


class Maintainer(Base):
    __tablename__ = "maintainers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    address_id = Column(Integer, ForeignKey("address.id"), nullable=False)
    is_business = Column(Boolean, nullable=False, default=False)
    client_id = Column(String, nullable=True)  # Armazena o client_id da Pagar.me

    # Relationship definition
    address = relationship("Address")
    user = relationship("User")
    ongs = relationship("OngMaintainer", back_populates="maintainer")
    cards = relationship("Card", back_populates="maintainer")