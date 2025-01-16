from typing import Optional
from pydantic import BaseModel

class Maintainer(BaseModel):
    email: str = None
    name: str = None
    phone: int = None
    cpf: int = None
    birthday: str = None
    zip: str = None
    street: str = None
    neighborhood: str = None
    number: str = None
    complement: Optional[str] = None
    city: str = None
    state: str = None
    member_since: Optional[str] = None
    org_id: int = None
    role_id: int = None
    status: str = None