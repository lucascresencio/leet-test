from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.staff import Staff
from app.models.user import User
from app.schemas.address import AddressResponse
from app.schemas.staff import StaffCreate, StaffResponse
from app.schemas.user import UserResponse
from app.services.staff_service import create_staff
from app.config.database import get_db
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/staff", tags=["staff"])


@router.post("/create", response_model=StaffResponse)
def create_staff_endpoint(
        staff: StaffCreate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    # Apenas ONGs ou staffs podem criar novos staffs
    if current_user["type"] not in ["ong", "staff"]:
        raise HTTPException(status_code=403, detail="Permission denied")

    db_staff = create_staff(db, staff, current_user)

    # Serialização manual dos sub-objetos
    user_response = UserResponse.from_orm(db_staff.user)
    address_response = AddressResponse.from_orm(db_staff.address)
    response = StaffResponse(
        id=db_staff.id,
        user_id=db_staff.user_id,
        address_id=db_staff.address_id,
        name=db_staff.name,
        user=user_response,
        address=address_response,
        ong_id=db_staff.ong_id,
        role=db_staff.role.name
    )

    return response
