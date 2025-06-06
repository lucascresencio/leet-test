from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey

from app.config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, nullable=True)
    name = Column(String, nullable=True)
    document = Column(String, unique=True, nullable=True)
    phone_number = Column(String, unique=True, nullable=True)
    password = Column(String)
    status = Column(String, nullable=False, default="I")  # I: Inserted, A: Altered, E: Excluded
    user_type_id = Column(Integer, ForeignKey("user_types.id"), nullable=False)
    photo = Column(String, nullable=True)

    user_type = relationship("UserType")

class UserType(Base):
    __tablename__ = "user_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # Ex.: "staff", "maintainer", "ong"