from sqlalchemy.orm import Session
from app.models.ong import ONG
from app.models.address import Address
from app.schemas.ong import ONGCreate


def create_ong(db: Session, ong: ONGCreate, address: dict):
    db_ong = ONG(name=ong.name, cnpj=ong.cnpj)
    db.add(db_ong)
    db.commit()
    db.refresh(db_ong)

    db_address = Address(**address, entity_id=db_ong.id, entity_type="ong")
    db.add(db_address)
    db.commit()
    return db_ong