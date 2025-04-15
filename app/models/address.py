from sqlalchemy import Column, Integer, String
from app.config.database import Base


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String)
    street_number = Column(String)
    complementary = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)