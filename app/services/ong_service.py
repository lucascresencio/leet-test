from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.ong import ONG
from app.models.address import Address
from app.models.user import UserType, User
from app.schemas.ong import ONGCreate
from app.services.auth_service import get_password_hash


def create_ong(db: Session, ong: ONGCreate, address: dict):

    # Create address
    db_address = Address(**ong.address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)

    ong_type = db.query(UserType).filter(UserType.name == "ong").first()
    if not ong_type:
        raise HTTPException(status_code=500, detail="User type 'ong' not found")

    # Create user for ong
    db_user = User(
        username=ong.user.username,
        password=get_password_hash(ong.user.password),
        user_type_id=ong_type.id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create ong and associate do address and user
    db_ong = ONG(
        name=ong.name,
        document=ong.document,
        address_id=db_address.id,
        user_id=db_user.id
    )
    db.add(db_ong)
    db.commit()
    db.refresh(db_ong)
    return db_ong

def get_ong_by_id(db: Session, id: int):
    return db.query(ONG).filter(ONG.id == id).first()