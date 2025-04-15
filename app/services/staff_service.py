from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.ong import ONG
from app.models.staff import Staff
from app.models.roles import Role
from app.models.user import User, UserType
from app.models.address import Address
from app.schemas.address import AddressResponse
from app.schemas.role import RoleResponse
from app.schemas.staff import StaffCreate, StaffResponse
from app.schemas.user import UserResponse
from app.services.auth_service import get_password_hash
import logging

# Configuração do logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


def create_staff(db: Session, staff: StaffCreate, current_user: dict):
    logger.debug(f"Current user: {current_user}")
    logger.debug(f"Staff data: {staff.dict()}")

    # Verificar permissões
    if current_user["type"] not in ["staff", "ong"] or (current_user["type"] == "staff" and current_user.get("role") != "admin"):
        logger.error(f"Permission denied for user type: {current_user['type']}, role: {current_user.get('role')}")
        raise HTTPException(status_code=403, detail="Permission denied: only Staff (admin) or ONG can create staff")

    # Criar usuário
    user_type = db.query(UserType).filter(UserType.name == "staff").first()
    if not user_type:
        logger.error("User type 'staff' not found")
        raise HTTPException(status_code=500, detail="User type 'staff' not found")

    db_user = User(
        username=staff.user.username,
        password=get_password_hash(staff.user.password),
        user_type_id=user_type.id,
        name=staff.user.name,
        document=staff.user.document,
        email=staff.user.email,
        phone_number=staff.user.phone_number,
        status="I"
    )
    db.add(db_user)
    db.flush()

    # Criar endereço
    db_address = Address(**staff.address.dict())
    db.add(db_address)
    db.flush()

    # Determinar ong_id
    if current_user.get("role") == "admin":  # Admin staff
        if not staff.ong_id:
            logger.error("ong_id is required for admin")
            raise HTTPException(status_code=400, detail="ong_id is required for admin")
        ong_id = staff.ong_id
        ong = db.query(ONG).filter(ONG.id == ong_id).first()
        if not ong:
            logger.error(f"ONG not found for ong_id: {ong_id}")
            raise HTTPException(status_code=404, detail=f"ONG with id {ong_id} not found")
    else:  # ong
        user_id = current_user["user_id"] if "user_id" in current_user else current_user["user"].id
        ong = db.query(ONG).filter(ONG.user_id == user_id).first()
        if not ong:
            logger.error(f"ONG not found for user_id: {user_id}")
            raise HTTPException(status_code=400, detail="ONG not found for current user")
        ong_id = ong.id

    # Verificar se o role_id existe (staff.role_id é string, mas Role.id é int)
    role = db.query(Role).filter(Role.name == staff.role_id).first()
    if not role:
        logger.error(f"Role not found for role_id: {staff.role_id}")
        raise HTTPException(status_code=404, detail=f"Role with id {staff.role_id} not found")
    logger.debug(f"Role found: id={role.id}, name={role.name}")

    # Criar staff com role_id
    db_staff = Staff(
        user_id=db_user.id,
        ong_id=ong_id,
        role_id=role.id,
        address_id=db_address.id
    )
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)

    # Retornar resposta corrigida
    return StaffResponse(
        id=db_staff.id,
        user_id=db_staff.user_id,
        ong_id=db_staff.ong_id,
        role_id=str(db_staff.role_id),  # Converter para string para o schema
        role=RoleResponse(
            id=db_staff.role.id,  # RoleResponse espera int
            name=db_staff.role.name
        ),
        address_id=db_staff.address_id,
        address=AddressResponse(
            id=db_staff.address.id,
            street=db_staff.address.street,
            city=db_staff.address.city,
            state=db_staff.address.state,
            zip_code=db_staff.address.zip_code
        ) if db_staff.address else None,
        user=UserResponse(
            id=db_staff.user.id,
            username=db_staff.user.username,
            name=db_staff.user.name,
            document=db_staff.user.document,
            email=db_staff.user.email,
            phone_number=db_staff.user.phone_number,
            user_type=db_staff.user.user_type.name,
            status=db_staff.user.status,
            photo=db_staff.user.photo
        )
    )


def get_staff(
        db: Session,
        current_user: dict,
        ong_id: Optional[int] = None,
        status: Optional[str] = None,
        username: Optional[str] = None,
        name: Optional[str] = None,
        document: Optional[str] = None,
        email: Optional[str] = None,
        phone_number: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
) -> list[StaffResponse]:
    if current_user["type"] not in ["admin", "ong", "staff"]:
        logger.error(f"Permission denied for user type: {current_user['type']}")
        raise HTTPException(status_code=403, detail="Permission denied: only ONG or Staff can list staff")

    query = db.query(Staff).join(User)

    if ong_id:
        query = query.filter(Staff.ong_id == ong_id)
        if current_user["type"] == "staff":
            user_staff = db.query(Staff).filter(Staff.user_id == current_user["id"]).first()
            if not user_staff or user_staff.ong_id != ong_id:
                raise HTTPException(status_code=403,
                                    detail="Permission denied: staff can only list staff from their own ONG")
        logger.debug(f"Filtro aplicado: ong_id={ong_id}")
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

    staff_list = query.offset(skip).limit(limit).all()
    return [
        StaffResponse(
            id=staff.id,
            user_id=staff.user_id,
            ong_id=staff.ong_id,
            role_id=str(staff.role_id),  # Converter para string para o schema
            role=RoleResponse(
                id=staff.role.id,  # RoleResponse espera int
                name=staff.role.name
            ),
            address_id=staff.address_id,
            address=AddressResponse(
                id=staff.address.id,
                street=staff.address.street,
                city=staff.address.city,
                state=staff.address.state,
                zip_code=staff.address.zip_code
            ) if staff.address else None,
            user=UserResponse(
                id=staff.user.id,
                username=staff.user.username,
                name=staff.user.name,
                document=staff.user.document,
                email=staff.user.email,
                phone_number=staff.user.phone_number,
                user_type=staff.user.user_type.name,
                status=staff.user.status,
                photo=staff.user.photo
            )
        ) for staff in staff_list
    ]


def get_staff_by_id(db: Session, staff_id: int) -> StaffResponse:
    staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    return StaffResponse(
        id=staff.id,
        user_id=staff.user_id,
        ong_id=staff.ong_id,
        user=UserResponse(
            id=staff.user.id,
            username=staff.user.username,
            name=staff.user.name,
            document=staff.user.document,
            email=staff.user.email,
            phone_number=staff.user.phone_number,
            user_type=staff.user.user_type.name,
            status=staff.user.status,
            photo=staff.user.photo
        )
    )