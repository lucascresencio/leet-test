from pydantic import BaseModel


class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str


class AddressCreate(AddressBase):
    pass


class AddressResponse(AddressBase):
    id: int

    class Config:
        from_attributes = True