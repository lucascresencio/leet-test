from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.ong import ONGCreate, ONGResponse
from app.schemas.address import AddressCreate
from app.services.ong_service import create_ong
from app.config.database import get_db

router = APIRouter(prefix="/ongs", tags=["ongs"])

@router.post("/", response_model=ONGResponse)
def create_new_ong(
    ong: ONGCreate,
    address: AddressCreate,
    db: Session = Depends(get_db)
):
    return create_ong(db, ong, address.dict())