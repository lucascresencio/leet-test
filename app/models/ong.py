from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base


class ONG(Base):
    __tablename__ = "ongs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    document = Column(String, unique=True, nullable=False)
    address_id = Column(Integer, ForeignKey("address.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship definition
    address = relationship("Address")
    user = relationship("User")
    maintainers = relationship("Maintainer", secondary="ong_maintainer")

# Associative table OngMaintainer
class OngMaintainer(Base):
    __tablename__ = "ong_maintainer"
    ong_id = Column(Integer, ForeignKey("ongs.id"), primary_key=True)
    maintainer_id = Column(Integer, ForeignKey("maintainers.id"), primary_key=True)

    #Relationship
    ong = relationship("ONG")
    maintainer = relationship("Maintainer")