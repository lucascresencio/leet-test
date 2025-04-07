from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.user import User, UserType
from app.schemas.user import UserResponse
from app.config.database import get_db
from app.services.auth_service import get_current_user
from typing import Optional

from app.services.user_service import search_users, get_user_by_id, delete_user, update_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/search/", response_model=list[UserResponse])
def search_users_endpoint(
        name: Optional[str] = None,
        photo: Optional[str] = None,
        username: Optional[str] = None,
        document: Optional[str] = None,
        email: Optional[str] = None,
        phone_number: Optional[str] = None,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    if current_user["type"] not in ["ong", "staff"]:
        raise HTTPException(status_code=403, detail="Permission denied")

    return search_users(db, name, username, document, email, phone_number)


@router.get("/{id}", response_model=UserResponse)
def get_user_by_id_endpoint(
        id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    if current_user["type"] not in ["ong", "staff"]:
        raise HTTPException(status_code=403, detail="Permission denied")

    return get_user_by_id(db, id)


@router.put("/{id}", response_model=UserResponse)
def update_user_endpoint(
        id: int,
        username: Optional[str] = None,
        document: Optional[str] = None,
        email: Optional[str] = None,
        phone_number: Optional[str] = None,
        photo: Optional[str] = None,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    if current_user["type"] not in ["ong", "staff"]:
        raise HTTPException(status_code=403, detail="Permission denied")

    update_data = {
        "username": username,
        "document": document,
        "email": email,
        "phone_number": phone_number,
        "photo": photo
    }
    return update_user(db, id, update_data)


@router.delete("/{id}", response_model=UserResponse)
def delete_user_endpoint(
        id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    if current_user["type"] not in ["ong", "staff"]:
        raise HTTPException(status_code=403, detail="Permission denied")

    return delete_user(db, id)