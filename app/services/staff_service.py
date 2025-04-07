from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.ong import ONG
from app.models.staff import Staff
from app.models.roles import Role
from app.models.user import User, UserType
from app.models.address import Address
from app.schemas.staff import StaffCreate, StaffResponse
from app.services.auth_service import get_password_hash
import logging

# Configuração do logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


def create_staff(db: Session, staff: StaffCreate, current_user: dict) -> Staff:
    logger.debug(f"Creating staff with data: {staff.dict()}")

    try:
        # Validar a role
        valid_roles = ["admin", "office"]
        if staff.role not in valid_roles:
            raise HTTPException(status_code=400, detail="Invalid role. Must be 'admin', 'office' ")

        # Verificar se a ONG existe
        ong = db.query(ONG).filter(ONG.id == staff.ong_id).first()
        if not ong:
            raise HTTPException(status_code=400, detail=f"ONG with id {staff.ong_id} not found")

        # Criar o endereço
        db_address = Address(**staff.address.dict())
        db.add(db_address)
        db.flush()

        # Buscar o tipo "staff"
        staff_type = db.query(UserType).filter(UserType.name == "staff").first()
        if not staff_type:
            raise HTTPException(status_code=500, detail="User type 'staff' not found")

        # Criar o usuário
        db_user = User(
            username=staff.user.username.lower(),
            password=get_password_hash(staff.user.password),
            user_type_id=staff_type.id
        )
        db.add(db_user)
        db.flush()

        # Buscar o role_id
        db_role = db.query(Role).filter(Role.name == staff.role).first()
        if not db_role:
            raise HTTPException(status_code=400, detail=f"Role '{staff.role}' not found")

        # Criar o staff
        db_staff = Staff(
            ong_id=staff.ong_id,
            address_id=db_address.id,
            user_id=db_user.id,
            role_id=db_role.id
        )
        db.add(db_staff)


        db.commit()
        db.refresh(db_address)
        db.refresh(db_user)
        db.refresh(db_staff)

        logger.debug(f"Created address: {db_address.__dict__}")
        logger.debug(f"Created user: {db_user.__dict__}")
        logger.debug(f"Created staff: {db_staff.__dict__}")

        return db_staff

    except HTTPException as e:
        db.rollback()
        logger.error(f"Error creating staff: {e.detail}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error creating staff: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")