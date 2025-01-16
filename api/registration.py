from db.connection import supabase_connection

from api.models import Maintainer, Mobilizer

from fastapi import APIRouter

router = APIRouter()

# role_id rules:
# 1 : admin
# 2 : finance_staff
# 3 : office_staff
# 4 : maintainer
# 5 : mobilizer
# 6 : volunteer

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
         "role_id": 4,
         "status": maintainer.status,
         "fk_address": address_id
         }
    ]).execute()

    response = supabase_connection().table("maintainer").insert([{
        "member_since": maintainer.member_since,
        "fk_user": response_auth.user.id
    }]).execute()

    return response

# create mobilizer user
@router.post("/mobilizers")
def create_maintainer(mobilizer: Mobilizer):
    # auth user - create account
    response_auth = supabase_connection().auth.sign_up(
        {"email": mobilizer.email, "password": "leet123"}
    )

    response_address = supabase_connection().table("address").insert([{
        "street": mobilizer.street,
        "neighborhood": mobilizer.neighborhood,
        "zip": mobilizer.zip,
        "complement": mobilizer.complement,
        "number": mobilizer.number,
        "city": mobilizer.city,
        "state": mobilizer.state
    }]).execute()

    for address in response_address.data:
        address_id = address["id"]

    response = supabase_connection().table("profile").insert([
        {"name": mobilizer.name,
         "fk_user": response_auth.user.id,
         "phone": mobilizer.phone,
         "cpf_cnpj": mobilizer.cpf,
         "birthday": mobilizer.birthday,
         "fk_org": mobilizer.org_id,
         "role_id": 5,
         "status": mobilizer.status,
         "fk_address": address_id
         }
    ]).execute()

    response = supabase_connection().table("mobilizer").insert([{
        "member_since": mobilizer.member_since,
        "fk_user": response_auth.user.id
    }]).execute()

    return response