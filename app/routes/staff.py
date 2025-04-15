from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.staff import Staff
from app.models.user import User
from app.schemas.address import AddressResponse
from app.schemas.staff import StaffCreate, StaffResponse
from app.schemas.user import UserResponse
from app.services.staff_service import create_staff, get_staff_by_id, get_staff
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

    response = create_staff(db, staff, current_user)

    return response

@router.get("/filter/", response_model=list[StaffResponse])
def get_staff_endpoint(
    ong_id: Optional[int] = None,
    status: Optional[str] = None,
    username: Optional[str] = None,
    name: Optional[str] = None,
    document: Optional[str] = None,
    email: Optional[str] = None,
    phone_number: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return get_staff(db, current_user, ong_id, status, username, name,
                     document, email, phone_number, skip, limit)

@router.get("/{staff_id}", response_model=StaffResponse)
def get_staff_by_id_endpoint(
    staff_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return get_staff_by_id(db, staff_id)
