from fastapi import HTTPException
from sqlalchemy import or_
from typing import Optional

from sqlalchemy.orm import Session
from app.models.user import User, UserType
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import get_password_hash

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


def get_user_by_id(db: Session, user_id: int) -> UserResponse:
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


def search_users(
        db: Session,
        username: Optional[str] = None,
        name: Optional[str] = None,
        document: Optional[str] = None,
        email: Optional[str] = None,
        phone_number: Optional[str] = None
) -> list[UserResponse]:
    query = db.query(User).join(UserType, User.user_type_id == UserType.id)
    filters = []
    if username:
        filters.append(User.username.ilike(f"%{username}%"))
    if name:
        filters.append(User.name.ilike(f"%{name}%"))
    if document:
        filters.append(User.document.ilike(f"%{document}%"))
    if email:
        filters.append(User.email.ilike(f"%{email}%"))
    if phone_number:
        filters.append(User.phone_number.ilike(f"%{phone_number}%"))

    if filters:
        query = query.filter(or_(*filters))

    users = query.all()
    return [
        UserResponse(
            id=user.id,
            username=user.username,
            name=user.name,
            document=user.document,
            email=user.email,
            phone_number=user.phone_number,
            user_type=user.user_type.name if user.user_type else None,
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