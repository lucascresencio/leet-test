from api import models
from datetime import datetime as dt
from db.connection import supabase_connection
from dotenv import load_dotenv
load_dotenv()

# create/authenticate account for a new user
async  def signup_user(payload: models.User):
    response_auth = supabase_connection().auth.sign_up(
        {"email": payload.email, "password": "leet123"}
    )

    return response_auth

# create new address
async def post_address(payload: models.Address):
    created_date = dt.now().strftime("%Y-%m-%d %H:%M")
    query = supabase_connection().table("address").insert([{
        "street": payload.street,
        "neighborhood": payload.neighborhood,
        "zip": payload.zip,
        "complement": payload.complement,
        "number": payload.number,
        "city": payload.city,
        "state": payload.state,
        "created_at": created_date
    }]).execute()

    return query

# create new profile
async def post_profile(payload: models.Profile):
    created_date = dt.now().strftime("%Y-%m-%d %H:%M")

    if payload.status is None:
        payload.status = "activated"

    query = supabase_connection().table("profile").insert([{
        "email": payload.email,
        "name": payload.name,
        "fk_org": payload.org_id,
        "role_id": payload.role_id,
        "cpf_cnpj": payload.cpf,
        "phone": payload.phone,
        "birthday": payload.birthday,
        "status": payload.status,
        "fk_user": payload.fk_user,
        "fk_address": payload.fk_address,
        "created_at": created_date
    }]).execute()

    return query

# create new maintainer - this action sigup an user, create an address, a profile and a maintainer
async def post_maintainer(payload_user: models.User, payload_profile: models.Profile,
                      payload_address: models.Address, payload_maintainer: models.Maintainer):
    created_date = dt.now().strftime("%Y-%m-%d %H:%M")

    # auth user - create account
    new_user = await signup_user(payload_user)
    user_id = new_user.user.id

    # create new address for user - (the relationship is on profile table)
    new_address = await post_address(payload_address)
    for address in new_address.data:
        new_address = address["id"]
    address_id = new_address

    payload_profile.fk_user = user_id
    payload_profile.fk_address = address_id
    #It has to be 4 because the user is a maintainer
    payload_profile.role_id = 4
    payload_maintainer.fk_user = user_id

    new_profile = await post_profile(payload_profile)

    new_maintainer = supabase_connection().table("maintainer").insert([{
        "member_since": payload_maintainer.member_since,
        "fk_user": payload_maintainer.fk_user,
        "created_at": created_date
    }]).execute()

    return new_user, new_profile, new_address, new_maintainer

# create new mobilizer - this action sigup an user, create an address, a profile and a mobilizer
async def post_mobilizer(payload_user: models.User, payload_profile: models.Profile,
                      payload_address: models.Address, payload_mobilizer: models.Mobilizer):
    created_date = dt.now().strftime("%Y-%m-%d %H:%M")

    # auth user - create account
    new_user = await signup_user(payload_user)
    user_id = new_user.user.id

    # create new address for user - (the relationship is on profile table)
    new_address = await post_address(payload_address)
    for address in new_address.data:
        new_address = address["id"]
    address_id = new_address

    payload_profile.fk_user = user_id
    payload_profile.fk_address = address_id
    # It has to be 5 because the user is a mobilizer
    payload_profile.role_id = 5
    payload_mobilizer.fk_user = user_id

    new_profile = await post_profile(payload_profile)

    new_mobilizer = supabase_connection().table("maintainer").insert([{
        "member_since": payload_mobilizer.member_since,
        "commission": payload_mobilizer.commission,
        "fk_user": payload_mobilizer.fk_user,
        "created_at": created_date
    }]).execute()

    return new_user, new_profile, new_address, new_mobilizer