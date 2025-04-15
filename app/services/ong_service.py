from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.ong import ONG  # Corrigido de ONG para Ong (consistência)
from app.models.address import Address
from app.models.staff import Staff
from app.models.user import UserType, User
from app.schemas.address import AddressResponse
from app.schemas.ong import ONGCreate, ONGResponse
from app.schemas.user import UserResponse
from app.services.auth_service import get_password_hash
import logging

# Configuração explícita do logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


def create_ong(db: Session, ong: ONGCreate, current_user: dict):
    # Verificar permissões
    if current_user["type"] not in ["admin", "ong", "staff"]:
        logger.error(f"Permission denied for user type: {current_user['type']}")
        raise HTTPException(status_code=403, detail="Permission denied: only Admin, ONG, or Staff can create ONGs")

    try:
        # Criar endereço
        db_address = Address(**ong.address.dict())
        db.add(db_address)
        db.flush()
        db.refresh(db_address)
        logger.debug(f"Address created with id: {db_address.id}")

        # Buscar o tipo "ong"
        ong_type = db.query(UserType).filter(UserType.name == "ong").first()
        if not ong_type:
            logger.error("User type 'ong' not found")
            raise HTTPException(status_code=500, detail="User type 'ong' not found")

        # Criar usuário para a ONG
        db_user = User(
            username=ong.user.username,
            name=ong.user.name,
            document=ong.user.document,
            phone_number=ong.user.phone_number,
            photo=ong.user.photo,
            password=get_password_hash(ong.user.password),
            user_type_id=ong_type.id,
            status="I"  # Adicionado para consistência com o padrão
        )
        db.add(db_user)
        db.flush()
        db.refresh(db_user)
        logger.debug(f"User created with id: {db_user.id}")

        # Criar ONG e associar endereço e usuário
        db_ong = ONG(
            address_id=db_address.id,
            user_id=db_user.id,
            description=ong.description
        )
        db.add(db_ong)
        db.flush()
        db.refresh(db_ong)
        logger.debug(f"ONG created with id: {db_ong.id}")

        # Serializar UserResponse manualmente
        user_response = UserResponse(
            id=db_user.id,
            username=db_user.username,
            name=db_user.name,
            document=db_user.document,
            email=db_user.email,
            phone_number=db_user.phone_number,
            user_type=db_user.user_type.name,  # Extrair o nome como string
            status=db_user.status,
            photo=db_user.photo
        )

        db.commit()

        # Retornar OngResponse com UserResponse
        return ONGResponse(
            id=db_ong.id,
            user_id=db_ong.user_id,
            description=db_ong.description,
            user=user_response,
            address=AddressResponse.from_orm(db_address)
        )


    except Exception as e:
        db.rollback()
        logger.error(f"Error creating ONG: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create ONG: {str(e)}")


def get_ongs(
        db: Session,
        current_user: dict,
        description: Optional[str] = None,
        status: Optional[str] = None,
        username: Optional[str] = None,
        name: Optional[str] = None,
        document: Optional[str] = None,
        email: Optional[str] = None,
        phone_number: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
) -> list[ONGResponse]:

    if current_user["type"] not in ["admin", "ong", "staff"]:
        logger.error(f"Permission denied for user type: {current_user['type']}")
        raise HTTPException(status_code=403, detail="Permission denied: only ONG or Staff can list ONGs")

    query = db.query(ONG).join(User)
    # Obter o ID do usuário de forma segura
    user_id = None
    if "user_id" in current_user:  # Caso ong
        user_id = current_user["user_id"]
    elif "user" in current_user and current_user["user"]:  # Caso staff ou maintainer
        user_id = current_user["user"].id


    if current_user["type"] == "staff" and current_user["role"] != "admin":
        user_staff = db.query(Staff).filter(Staff.user_id == user_id).first()
        if not user_staff:
            raise HTTPException(status_code=403, detail="Permission denied: staff not associated with any ONG")
        query = query.filter(ONG.id == user_staff.ong_id)

    if description:
        query = query.filter(ONG.description.ilike(f"%{description}%"))
        logger.debug(f"Filtro aplicado: description={description}")
    if status:
        query = query.filter(User.status == status)
        logger.debug(f"Filtro aplicado: status={status}")
    if username:
        query = query.filter(User.username.ilike(f"%{username}%"))
        logger.debug(f"Filtro aplicado: username={username}")
    if name:
        query = query.filter(User.name.ilike(f"%{name}%"))
        logger.debug(f"Filtro aplicado: name={name}")
    if document:
        query = query.filter(User.document.ilike(f"%{document}%"))
        logger.debug(f"Filtro aplicado: document={document}")
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
        logger.debug(f"Filtro aplicado: email={email}")
    if phone_number:
        query = query.filter(User.phone_number.ilike(f"%{phone_number}%"))
        logger.debug(f"Filtro aplicado: phone_number={phone_number}")

    ongs = query.offset(skip).limit(limit).all()
    return [
        ONGResponse(
            id=ong.id,
            user_id=ong.user_id,
            address_id=ong.address_id,
            description=ong.description,
            user=UserResponse(
                id=ong.user.id,
                username=ong.user.username,
                name=ong.user.name,
                document=ong.user.document,
                email=ong.user.email,
                phone_number=ong.user.phone_number,
                user_type=ong.user.user_type.name,
                status=ong.user.status,
                photo=ong.user.photo
            ),
            address=AddressResponse.from_orm(ong.address)
        ) for ong in ongs
    ]

# Buscar pelo id
def get_ong_by_id(db: Session, id: int):
    ong = db.query(ONG).filter(ONG.id == id).first()
    if not ong:
        raise HTTPException(status_code=404, detail="ONG not found")
    return ONGResponse(
        id=ong.id,
        user_id=ong.user_id,
        address_id=ong.address_id,
        description=ong.description,
        user=UserResponse(
            id=ong.user.id,
            username=ong.user.username,
            name=ong.user.name,
            document=ong.user.document,
            email=ong.user.email,
            phone_number=ong.user.phone_number,
            user_type=ong.user.user_type.name,
            status=ong.user.status,
            photo=ong.user.photo
        ),
        address=AddressResponse.from_orm(ong.address)
    )