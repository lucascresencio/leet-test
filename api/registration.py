from db.connection import supabase_connection

from api.models import Maintainer

from fastapi import APIRouter

router = APIRouter()

# create maintainer user
@router.post("/maintainers")
def create_maintainer(maintainer: Maintainer):
    # auth user - create account
    response_auth = supabase_connection().auth.sign_up(
        {"email": maintainer.email, "password": "leet123"}
    )

    response_address = supabase_connection().table("address").insert([{
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

    response = supabase_connection().table("profile").insert([
        {"name": maintainer.name,
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

    response = supabase_connection().table("maintainer").insert([{
        "member_since": maintainer.member_since,
        "fk_user": response_auth.user.id
    }]).execute()

    return response