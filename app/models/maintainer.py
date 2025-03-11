from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base


class Maintainer(Base):
    __tablename__ = "maintainers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    address_id = Column(Integer, ForeignKey("address.id"), nullable=False)

    # Relationship definition
    address = relationship("Address")
    user = relationship("User")