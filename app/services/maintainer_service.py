from sqlalchemy.orm import Session
from app.models.maintainer import Maintainer
from app.models.address import Address
from app.schemas.maintainer import MaintainerCreate
from app.services.auth_service import get_password_hash
from ..models.user import User
from ..schemas.address import AddressCreate


def create_maintainer(db: Session, maintainer: MaintainerCreate, address: AddressCreate):
    # Criar o endereço
    db_address = Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)

    # Criar o usuário associado ao mantenedor
    db_user = User(
        username=maintainer.user.username,
        password=get_password_hash(maintainer.user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Criar o mantenedor associando endereço e usuário
    db_maintainer = Maintainer(
        name=maintainer.name,
        address_id=db_address.id,
        user_id=db_user.id
    )
    db.add(db_maintainer)
    db.commit()
    db.refresh(db_maintainer)
    return db_maintainer

