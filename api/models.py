from typing import Optional
from pydantic import BaseModel

class ResponsePost(BaseModel):
    id: int
    msg: str

class User(BaseModel):
    email: str = None

class Profile(BaseModel):
    email: str = None
    name: str = None
    phone: int = None
    cpf: int = None
    birthday: Optional[str] = None
    org_id: int = None
    role_id: int = None
    status: Optional[str] = None

class Maintainer(BaseModel):
    member_since: Optional[str] = None

class Mobilizer(BaseModel):
    member_since: Optional[str] = None
    commission: Optional[float] = None

class Address(BaseModel):
    zip: str = None
    street: str = None
    neighborhood: str = None
    number: str = None
    complement: Optional[str] = None
    city: str = None
    state: str = None
