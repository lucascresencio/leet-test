from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.maintainer import Maintainer
from app.models.address import Address
from app.schemas.maintainer import MaintainerCreate
from app.services.auth_service import get_password_hash, get_current_user
from ..config.database import get_db
from ..models.user import User, UserType
from ..schemas.address import AddressCreate


def create_maintainer(db: Session, maintainer: MaintainerCreate, current_user: dict):

    # Create address
    db_address = Address(**maintainer.address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)

    maintainer_type = db.query(UserType).filter(UserType.name == "maintainer").first()
    if not maintainer_type:
        raise HTTPException(status_code=500, detail="User type 'maintainer' not found")

    # Create user for maintainer
    db_user = User(
        username=maintainer.user.username,
        password=get_password_hash(maintainer.user.password),
        user_type_id=maintainer_type.id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create maintainer and associate do address and user
    db_maintainer = Maintainer(
        name=maintainer.name,
        address_id=db_address.id,
        user_id=db_user.id
    )
    db.add(db_maintainer)
    db.commit()
    db.refresh(db_maintainer)
    return db_maintainer