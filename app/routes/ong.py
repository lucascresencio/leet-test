from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.address import AddressResponse
from app.schemas.ong import ONGCreate, ONGResponse
from app.schemas.user import UserResponse
from app.services.ong_service import create_ong
from app.config.database import get_db

router = APIRouter(prefix="/ongs", tags=["ongs"])

@router.post("/create", response_model=ONGResponse)
def create_new_ong(
    ong: ONGCreate,
    db: Session = Depends(get_db),
):
    db_ong = create_ong(db, ong, ong.address.dict())

    # Serialização manual dos sub-objetos
    user_response = UserResponse.from_orm(db_ong.user)
    address_response = AddressResponse.from_orm(db_ong.address)
    response = ONGResponse(
        id=db_ong.id,
        user_id=db_ong.user_id,
        address_id=db_ong.address_id,
        name=db_ong.name,
        user=user_response,
        address=address_response
    )
    return response
    #return create_ong(db, ong, ong.address.dict())

# @router.get("/get/{ong_id}", response_model=ONGResponse)
# def get_ong(ong_id: int, db: Session = Depends(get_db)):
#     ong = db.query(ONG).filter(ONG.id == ong_id).first()
#     if not ong:
#         raise HTTPException(status_code=404, detail="ONG not found")
#     return ong