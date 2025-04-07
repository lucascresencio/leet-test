import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.base import Base, BasePhoto, BaseVolunteer
from app.models.address import Address
from app.models.volunteer import Volunteer
from app.schemas.address import AddressResponse
from app.schemas.base import BaseCreate, BaseUpdate, BaseResponse, BaseVolunteerResponse, BasePhotoResponse

# Configuração explícita do logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def create_base(db: Session, base: BaseCreate, current_user: dict) -> BaseResponse:
    # Verificar permissões
    if current_user["type"] not in ["admin", "ong", "staff"]:
        logger.error(f"Permission denied for user type: {current_user['type']}")
        raise HTTPException(status_code=403, detail="Permission denied: only ONG or Staff can create bases")

    try:
        # Log dos dados recebidos
        logger.debug(f"Dados recebidos no schema BaseCreate: {base.dict()}")

        # Criar endereço
        db_address = Address(**base.address.dict())
        db.add(db_address)
        db.flush()
        db.refresh(db_address)
        logger.debug(f"Address created with id: {db_address.id}")

        # Criar base com os dados do schema
        db_base = Base()
        db_base.ong_id = base.ong_id
        db_base.address_id = db_address.id
        db_base.name = base.name
        db_base.foundation_date = base.foundation_date
        db_base.email = base.email
        db_base.phone_number = base.phone_number
        db_base.main_photo = base.main_photo
        db_base.notes = base.notes
        db_base.status = "I"

        # Log dos valores após atribuição
        logger.debug(f"Valores atribuídos ao db_base antes de adicionar: {vars(db_base)}")

        db.add(db_base)
        db.flush()
        logger.debug(f"Base created with id: {db_base.id}, valores após flush: {vars(db_base)}")

        # Adicionar fotos
        for photo_url in base.photo_urls:
            db_photo = BasePhoto(base_id=db_base.id, photo_url=photo_url)
            db.add(db_photo)
            logger.debug(f"Photo added: {photo_url}")

        # Adicionar voluntários e preparar a lista para resposta
        volunteers_response = []
        for volunteer_id in base.volunteer_ids:
            db_volunteer = BaseVolunteer(base_id=db_base.id, volunteer_id=volunteer_id)
            db.add(db_volunteer)
            db.flush()  # Garantir que o voluntário seja persistido
            logger.debug(f"Volunteer added: {volunteer_id}")

            # Carregar o nome do voluntário
            volunteer = db.query(Volunteer).filter(Volunteer.id == volunteer_id).first()
            if volunteer:
                volunteers_response.append(
                    BaseVolunteerResponse(
                        id=db_volunteer.id,
                        base_id=db_base.id,
                        volunteer_id=volunteer_id,
                        volunteer_name=volunteer.name,
                        joined_at=db_volunteer.joined_at
                    )
                )

        db.commit()
        logger.debug(f"Antes do commit, valores de db_base: {vars(db_base)}")
        db.refresh(db_base)
        logger.debug(f"Base {db_base.id} committed successfully")

        # Construir a resposta manualmente
        base_response = BaseResponse(
            id=db_base.id,
            ong_id=db_base.ong_id,
            address_id=db_base.address_id,
            name=db_base.name,
            foundation_date=db_base.foundation_date,
            email=db_base.email,
            phone_number=db_base.phone_number,
            main_photo=db_base.main_photo,
            notes=db_base.notes,
            status=db_base.status,
            created_at=db_base.created_at,
            updated_at=db_base.updated_at,
            address=AddressResponse.from_orm(db_address),
            photos=[BasePhotoResponse.from_orm(photo) for photo in db_base.photos],
            volunteers=volunteers_response
        )

        return base_response

    except Exception as e:
        db.rollback()
        logger.error(f"Error creating base: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create base: {str(e)}")

def get_base(db: Session, base_id: int) -> BaseResponse:
    base = db.query(Base).filter(Base.id == base_id, Base.status != "E").first()
    if not base:
        raise HTTPException(status_code=404, detail="Base not found or excluded")
    return base

def get_bases(db: Session, skip: int = 0, limit: int = 100) -> list[BaseResponse]:
    return db.query(Base).filter(Base.status != "E").offset(skip).limit(limit).all()

def update_base(db: Session, base_id: int, base_update: BaseUpdate, current_user: dict) -> BaseResponse:
    if current_user["type"] not in ["ong", "staff"]:
        raise HTTPException(status_code=403, detail="Permission denied: only ONG or Staff can update bases")

    base = db.query(Base).filter(Base.id == base_id, Base.status != "E").first()
    if not base:
        raise HTTPException(status_code=404, detail="Base not found or excluded")

    update_data = base_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(base, key, value)
    base.status = "A"

    db.commit()
    db.refresh(base)
    return base

def delete_base(db: Session, base_id: int, current_user: dict) -> BaseResponse:
    if current_user["type"] not in ["ong", "staff"]:
        raise HTTPException(status_code=403, detail="Permission denied: only ONG or Staff can delete bases")

    base = db.query(Base).filter(Base.id == base_id, Base.status != "E").first()
    if not base:
        raise HTTPException(status_code=404, detail="Base not found or excluded")

    base.status = "E"
    db.commit()
    db.refresh(base)
    return base