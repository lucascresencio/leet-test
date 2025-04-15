from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.address import AddressResponse
from app.schemas.ong import ONGCreate, ONGResponse
from app.schemas.user import UserResponse
from app.services.ong_service import create_ong, get_ong_by_id, get_ongs
from app.config.database import get_db
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/ongs", tags=["ongs"])

@router.post("/create", response_model=ONGResponse)  # Usar OngResponse
def create_ong_endpoint(ong: ONGCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return create_ong(db, ong, current_user)

@router.get("/filter/", response_model=list[ONGResponse])
def get_ongs_endpoint(
    description: Optional[str] = None,
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
    return get_ongs(db, current_user, description, status, username,
                    name, document, email, phone_number, skip, limit)

@router.get("/{ong_id}", response_model=ONGResponse)
def get_ong_by_id_endpoint(
    ong_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return get_ong_by_id(db, ong_id)