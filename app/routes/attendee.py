from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.attendee import AttendeeCreate, AttendeeUpdate, AttendeeResponse
from app.services.attendee_service import create_attendee, get_attendee, get_attendees, update_attendee, delete_attendee
from app.config.database import get_db
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/attendees", tags=["attendees"])

@router.post("/create", response_model=AttendeeResponse)
def create_attendee_endpoint(attendee: AttendeeCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return create_attendee(db, attendee, current_user)

@router.get("/{attendee_id}", response_model=AttendeeResponse)
def get_attendee_endpoint(attendee_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return get_attendee(db, attendee_id)

@router.get("/filter/", response_model=List[AttendeeResponse])
def get_attendees_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return get_attendees(db, skip, limit)

@router.put("/{attendee_id}", response_model=AttendeeResponse)
def update_attendee_endpoint(attendee_id: int, attendee: AttendeeUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return update_attendee(db, attendee_id, attendee, current_user)

@router.delete("/{attendee_id}", response_model=dict)
def delete_attendee_endpoint(attendee_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return delete_attendee(db, attendee_id, current_user)