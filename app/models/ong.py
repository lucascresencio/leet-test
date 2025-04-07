from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base


class ONG(Base):
    __tablename__ = "ongs"

    id = Column(Integer, primary_key=True, index=True)
    address_id = Column(Integer, ForeignKey("address.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    description = Column(String, nullable=True)

    # Relationship definition
    address = relationship("Address")
    user = relationship("User")
    maintainers = relationship("OngMaintainer", back_populates="ong")
    projects = relationship("Project", back_populates="ong")
    bases = relationship("Base", back_populates="ong")
    campaigns = relationship("Campaign", back_populates="ong")

# Associative table OngMaintainer
class OngMaintainer(Base):
    __tablename__ = "ong_maintainer"
    id = Column(Integer, primary_key=True, index=True)
    ong_id = Column(Integer, ForeignKey("ongs.id"), primary_key=True)
    maintainer_id = Column(Integer, ForeignKey("maintainers.id"), primary_key=True)

    #Relationship
    ong = relationship("ONG", back_populates="maintainers")
    maintainer = relationship("Maintainer", back_populates="ongs", overlaps="maintainers")  # Adicionado overlaps