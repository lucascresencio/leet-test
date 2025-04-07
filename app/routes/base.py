from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.base import BaseCreate, BaseUpdate, BaseResponse
from app.services.base_service import create_base, get_base, get_bases, update_base, delete_base
from app.config.database import get_db
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/bases", tags=["bases"])

@router.post("/create", response_model=BaseResponse)
def create_base_endpoint(base: BaseCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return create_base(db, base, current_user)

@router.get("/{base_id}", response_model=BaseResponse)
def get_base_endpoint(base_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return get_base(db, base_id)

@router.get("/filter/", response_model=List[BaseResponse])
def get_bases_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return get_bases(db, skip, limit)

@router.put("/{base_id}", response_model=BaseResponse)
def update_base_endpoint(base_id: int, base: BaseUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return update_base(db, base_id, base, current_user)

@router.delete("/{base_id}", response_model=BaseResponse)
def delete_base_endpoint(base_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return delete_base(db, base_id, current_user)