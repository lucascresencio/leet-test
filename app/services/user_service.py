from fastapi import HTTPException
from sqlalchemy import or_
from typing import Optional

from sqlalchemy.orm import Session
from app.models.user import User, UserType
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import get_password_hash
import logging

# Configuração do logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


def create_user(db: Session, user: dict, user_type_id: int) -> User:
    db_user = User(
        username=user["username"].lower(),
        password=get_password_hash(user["password"]),
        user_type_id=user_type_id,
        name=user.get("name"),  # Agora em users
        document=user.get("document"),
        email=user.get("email"),
        phone_number=user.get("phone_number"),
        status="I",
        photo=user.get("photo")
    )
    db.add(db_user)
    db.flush()
    return db_user


def get_user_by_id(db: Session, user_id: int, current_user: dict,) -> UserResponse:

    # Verificar permissão
    if current_user["type"] not in ["admin", "ong", "staff"]:
        logger.error(f"Permission denied for user type: {current_user['type']}")
        raise HTTPException(status_code=403, detail="Permission denied: only admin can list users")

    user = db.query(User).filter(User.id == user_id, User.status != "E").first()  # Exclui usuários com status "E"
    if not user:
        raise HTTPException(status_code=404, detail="User not found or excluded")

    return UserResponse(
        id=user.id,
        username=user.username,
        name=user.name,
        document=user.document,
        email=user.email,
        phone_number=user.phone_number,
        user_type=user.user_type.name if user.user_type else None,
        status=user.status,
        photo=user.photo
    )


def get_users(
        db: Session,
        current_user: dict,
        username: Optional[str] = None,
        user_type: Optional[str] = None,
        status: Optional[str] = None,
        name: Optional[str] = None,
        document: Optional[str] = None,
        email: Optional[str] = None,
        phone_number: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
) -> list[UserResponse]:

    # Verificar permissão
    if current_user["type"] not in ["admin", "ong", "staff"]:
        logger.error(f"Permission denied for user type: {current_user['type']}")
        raise HTTPException(status_code=403, detail="Permission denied: only admin can list users")

    query = db.query(User)

    if username:
        query = query.filter(User.username.ilike(f"%{username}%"))
    if user_type:
        query = query.join(UserType).filter(UserType.name == user_type)
    if status:
        query = query.filter(User.status == status)
    if name:
        query = query.filter(User.name == name)
    if document:
        query = query.filter(User.document == document)
    if email:
        query = query.filter(User.email == email)
    if phone_number:
        query = query.filter(User.phone_number == phone_number)

    users = query.offset(skip).limit(limit).all()

    return [
        UserResponse(
            id=user.id,
            username=user.username,
            name=user.name,
            document=user.document,
            email=user.email,
            phone_number=user.phone_number,
            user_type=user.user_type.name,
            status=user.status,
            photo=user.photo
        ) for user in users
    ]


def update_user(db: Session, user_id: int, update_data: dict) -> UserResponse:
    user = db.query(User).filter(User.id == user_id, User.status != "E").first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found or excluded")

    # Atualizar apenas os campos fornecidos
    for key, value in update_data.items():
        if value is not None:  # Ignorar valores None
            setattr(user, key, value)
    user.status = "A"  # Altera status para "Altered"

    db.commit()
    db.refresh(user)

    return UserResponse(
        id=user.id,
        username=user.username,
        name=user.name,
        document=user.document,
        email=user.email,
        phone_number=user.phone_number,
        user_type=user.user_type.name if user.user_type else None,
        status=user.status,
        photo=user.photo
    )


def delete_user(db: Session, user_id: int) -> UserResponse:
    user = db.query(User).filter(User.id == user_id, User.status != "E").first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found or already excluded")

    user.status = "E"  # Exclusão lógica
    db.commit()
    db.refresh(user)

    return UserResponse(
        id=user.id,
        username=user.username,
        name=user.name,
        document=user.document,
        email=user.email,
        phone_number=user.phone_number,
        user_type=user.user_type.name if user.user_type else None,
        status=user.status
    )