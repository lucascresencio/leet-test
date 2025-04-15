from sqlalchemy import Column, Integer, String, ForeignKey

from app.config.database import Base

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False) # Ex.: "admin", "office"