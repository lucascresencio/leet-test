from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client
from fastapi import FastAPI
from pydantic import BaseModel
os.environ['PYDANTIC_ERRORS_INCLUDE_URL'] = 'false'

app = FastAPI()

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
    complement: str = None
    city: str = None
    state: str = None
    member_since: str = None
    org_id: int = None
    role_id: int = None
    status: str = None


#connect to database
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

@app.get("/")
def root():
    return {"Leet Desenvolvimento de Programas de Computador LTDA"}

#create maintainer user
@app.post("/maintainers")
def create_maintainer(maintainer: Maintainer):
    #auth user - create account
    response_auth = supabase.auth.sign_up(
        {"email": maintainer.email, "password": "leet123"}
    )

    response_address = supabase.table("address").insert([{
        "street": maintainer.street,
        "neighborhood": maintainer.neighborhood,
        "zip": maintainer.zip,
        "complement": maintainer.complement,
        "number": maintainer.number,
        "city": maintainer.city,
        "state": maintainer.state
    }]).execute()
    
    for address in response_address.data:
        address_id = address["id"]


    response = supabase.table("profile").insert([
        { "name": maintainer.name,
          "fk_user": response_auth.user.id,
          "phone": maintainer.phone,
          "cpf_cnpj": maintainer.cpf,
          "birthday": maintainer.birthday,
          "fk_org": maintainer.org_id,
          "role_id": maintainer.role_id,
          "status": maintainer.status,
          "fk_address": address_id
        }
    ]).execute()

    response = supabase.table("maintainer").insert([{
        "member_since": maintainer.member_since,
        "fk_user": response_auth.user.id
    }]).execute()

    return response

