from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.address import AddressResponse
from app.schemas.ong import ONGCreate, ONGResponse
from app.schemas.user import UserResponse
from app.services.ong_service import create_ong, get_ong_by_id
from app.config.database import get_db
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/ongs", tags=["ongs"])

@router.post("/create", response_model=ONGResponse)  # Usar OngResponse
def create_ong_endpoint(ong: ONGCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return create_ong(db, ong, current_user)

@router.get("/{id}", response_model=ONGResponse)  # Usar OngResponse
def get_ong_by_id_endpoint(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    ong = get_ong_by_id(db, id)
    if not ong:
        raise HTTPException(status_code=404, detail="ONG not found")
    return ong