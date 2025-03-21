from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.maintainer import Maintainer
from app.models.ong import ONG, OngMaintainer
from app.models.address import Address
from app.schemas.maintainer import MaintainerCreate
from app.services.auth_service import get_password_hash, get_current_user
from ..config.database import get_db
from ..models.user import User, UserType
from ..schemas.address import AddressCreate
import logging


def create_maintainer(db: Session, maintainer: MaintainerCreate, current_user: dict):
    try:
        # Create address
        db_address = Address(**maintainer.address.dict())
        db.add(db_address)
        db.flush()

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
        db.flush()

        # Create maintainer and associate do address and user
        db_maintainer = Maintainer(
            name=maintainer.name,
            address_id=db_address.id,
            user_id=db_user.id,
            is_business=maintainer.is_business
        )
        db.add(db_maintainer)
        db.flush()

        # Verificar se o current_user é uma ONG
        if current_user["type"] == "ong":
            ong = db.query(ONG).filter(ONG.user_id == current_user["user_id"]).first()
            if not ong:
                logging.error(f"ONG not found for user_id: {current_user['user_id']}")
                raise HTTPException(status_code=400, detail="ONG not found for current user")

            # Criar relação na tabela ong_maintainer
            ong_maintainer = OngMaintainer(
                ong_id=ong.id,
                maintainer_id=db_maintainer.id
            )
            db.add(ong_maintainer)
            db.commit()

            db.refresh(db_address)
            db.refresh(db_user)
            db.refresh(db_maintainer)
            db.refresh(ong_maintainer)

            logging.debug(f"Created ong_maintainer relation: ong_id={ong.id}, maintainer_id={db_maintainer.id}")

        db.commit()

        db.refresh(db_address)
        db.refresh(db_user)
        db.refresh(db_maintainer)

        return db_maintainer
    except:
        raise HTTPException(status_code=400, detail="Creation of maintainer failed")