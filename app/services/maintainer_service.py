from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.maintainer import Maintainer
from app.models.ong import ONG, OngMaintainer
from app.models.address import Address
from app.schemas.maintainer import MaintainerCreate, MaintainerResponse
from app.services.auth_service import get_password_hash, get_current_user
from ..config.database import get_db
from ..models.user import User, UserType
from ..schemas.address import AddressCreate, AddressResponse
import logging

from ..schemas.user import UserResponse

# Configuração explícita do logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def create_maintainer(db: Session, maintainer: MaintainerCreate, current_user: dict):
    logger.debug(f"Current user: {current_user}")
    logger.debug(f"Maintainer data: {maintainer.dict()}")

    # Verificar permissões
    if current_user["type"] not in ["ong", "staff"]:
        logger.error(f"Permission denied for user type: {current_user['type']}")
        raise HTTPException(status_code=403, detail="Permission denied: only ONG or Staff can create maintainers")

    try:
        # Create address
        db_address = Address(**maintainer.address.dict())
        db.add(db_address)
        db.flush()
        logger.debug(f"Address created with id: {db_address.id}")

        maintainer_type = db.query(UserType).filter(UserType.name == "maintainer").first()
        if not maintainer_type:
            logger.error("User type 'maintainer' not found")
            raise HTTPException(status_code=500, detail="User type 'maintainer' not found")

        # Create user for maintainer
        db_user = User(
            username=maintainer.user.username.lower(),
            password=get_password_hash(maintainer.user.password),
            user_type_id=maintainer_type.id,
            name=maintainer.user.name,
            document=maintainer.user.document,
            email=maintainer.user.email,
            phone_number=maintainer.user.phone_number,
            photo=maintainer.user.photo,  # Foto agora em User
            status="I"
        )
        db.add(db_user)
        db.flush()
        logger.debug(f"User created with id: {db_user.id}")

        # Create maintainer and associate do address and user
        db_maintainer = Maintainer(
            address_id=db_address.id,
            user_id=db_user.id,
            is_business=maintainer.is_business
        )
        db.add(db_maintainer)
        db.flush()
        logger.debug(f"Maintainer created with id: {db_maintainer.id}")

        # Verificar se o current_user é uma ONG
        if current_user["type"] == "ong":
            ong = db.query(ONG).filter(ONG.user_id == current_user["user_id"]).first()
            if not ong:
                logger.error(f"ONG not found for user_id: {current_user['user_id']}")
                raise HTTPException(status_code=400, detail="ONG not found for current user")

            # Criar relação na tabela ong_maintainer
            ong_maintainer = OngMaintainer(
                ong_id=ong.id,
                maintainer_id=db_maintainer.id
            )
            db.add(ong_maintainer)
            db.flush()
            logger.debug(f"OngMaintainer created with ong_id: {ong.id}, maintainer_id: {db_maintainer.id}")

        db.commit()

        db.refresh(db_address)
        db.refresh(db_user)
        db.refresh(db_maintainer)

        logger.debug(f"Created address: {db_address.__dict__}")
        logger.debug(f"Created user: {db_user.__dict__}")
        logger.debug(f"Created maintainer: {db_maintainer.__dict__}")
        if current_user["type"] == "ong":
            logger.debug(f"Created ong_maintainer relation: ong_id={ong.id}, maintainer_id={db_maintainer.id}")

        return db_maintainer

    except HTTPException as e:
        db.rollback()
        logger.error(f"Error creating maintainer: {e.detail}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error creating maintainer: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create maintainer: {str(e)}")

def maintainers_list(
    db: Session = Depends(get_db),
):
    maintainers = db.query(Maintainer).join(User, Maintainer.user_id == User.id).filter(User.status != "E").all()

    # Manual Serialize
    response = [
        MaintainerResponse(
            id=m.id,
            user_id=m.user_id,
            address_id=m.address_id,
            is_business=m.is_business,
            user=UserResponse(
                id=m.user.id,
                username=m.user.username,
                name=m.user.name,
                document=m.user.document,
                email=m.user.email,
                phone_number=m.user.phone_number,
                user_type=m.user.user_type.name,
                status=m.user.status,
                foto=m.user.foto
            ),
            address=AddressResponse.from_orm(m.address)
        ) for m in maintainers
    ]

    return response