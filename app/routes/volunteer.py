from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.volunteer import VolunteerCreate, VolunteerUpdate, VolunteerResponse
from app.services.volunteer_service import create_volunteer, get_volunteer, get_volunteers, update_volunteer, delete_volunteer
from app.config.database import get_db
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/volunteers", tags=["volunteers"])

@router.post("/create", response_model=VolunteerResponse)
def create_volunteer_endpoint(volunteer: VolunteerCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return create_volunteer(db, volunteer, current_user)

@router.get("/{volunteer_id}", response_model=VolunteerResponse)
def get_volunteer_endpoint(volunteer_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return get_volunteer(db, volunteer_id)

@router.get("/filter/", response_model=List[VolunteerResponse])
def get_volunteers_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return get_volunteers(db, skip, limit)

@router.put("/{volunteer_id}", response_model=VolunteerResponse)
def update_volunteer_endpoint(volunteer_id: int, volunteer: VolunteerUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return update_volunteer(db, volunteer_id, volunteer, current_user)

@router.delete("/{volunteer_id}", response_model=dict)
def delete_volunteer_endpoint(volunteer_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return delete_volunteer(db, volunteer_id, current_user)