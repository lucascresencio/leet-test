from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.config.database import Base
from datetime import datetime


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    maintainer_id = Column(Integer, ForeignKey("maintainers.id"), nullable=False)
    card_id = Column(String, nullable=False, unique=True)  # ID do cartão na Pagar.me
    last_four_digits = Column(String(4), nullable=False)
    brand = Column(String, nullable=False)
    status = Column(String, nullable=False, default="active")  # active, inactive, expired
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    maintainer = relationship("Maintainer", back_populates="cards")