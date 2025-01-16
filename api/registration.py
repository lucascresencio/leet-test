from db.connection import supabase_connection
from datetime import datetime as dt

from api import models
from api import crud

from fastapi import APIRouter

router = APIRouter()

# role_id rules:
# 1 : admin
# 2 : finance_staff
# 3 : office_staff
# 4 : maintainer
# 5 : mobilizer
# 6 : volunteer

@router.post("/address", status_code=201)
async def create_address(payload: models.Address):
    address_id = await crud.post_address(payload)
    created_date = dt.now().strftime("%Y-%m-%d %H:%M")

    for address in address_id.data:
        address_id = address["id"]

    response_object = {
        "id": address_id,
        "created_at": created_date
    }
    return response_object


# create maintainer user
@router.post("/maintainers", status_code=201)
async def create_maintainer(payload_user: models.User, payload_profile: models.Profile,
                      payload_address: models.Address, payload_maintainer: models.Maintainer):

    new_maintainer = await crud.post_maintainer(payload_user, payload_profile,
                                                payload_address, payload_maintainer)

    return new_maintainer

# create mobilizer user
@router.post("/mobilizers", status_code=201)
async def create_mobilizer(payload_user: models.User, payload_profile: models.Profile,
                      payload_address: models.Address, payload_mobilizer: models.Mobilizer):

    new_mobilizer = await crud.post_mobilizer(payload_user, payload_profile,
                                                payload_address, payload_mobilizer)

    return new_mobilizer