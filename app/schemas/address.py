from typing import Optional

from pydantic import BaseModel


class AddressBase(BaseModel):
    street: str
    street_number: Optional[str] = None
    complementary: Optional[str] = None
    city: str
    state: str
    zip_code: str


class AddressCreate(AddressBase):
    street: str
    street_number: Optional[str] = None
    complementary: Optional[str] = None
    city: str
    state: str
    zip_code: str


class AddressResponse(AddressBase):
    id: int
    street: str
    street_number: Optional[str] = None
    complementary: Optional[str] = None
    city: str
    state: str
    zip_code: str

    class Config:
        from_attributes = True