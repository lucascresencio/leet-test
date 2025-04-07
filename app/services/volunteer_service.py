import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.volunteer import Volunteer
from app.models.address import Address
from app.schemas.volunteer import VolunteerCreate, VolunteerUpdate, VolunteerResponse

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

def create_volunteer(db: Session, volunteer: VolunteerCreate, current_user: dict) -> Volunteer:
    if current_user["type"] not in ["ong", "staff"]:
        raise HTTPException(status_code=403, detail="Permission denied")

    try:
        db_address = Address(**volunteer.address.dict())
        db.add(db_address)
        db.flush()

        db_volunteer = Volunteer(
            name=volunteer.name,
            photo=volunteer.photo,
            address_id=db_address.id,
            birthdate=volunteer.birthdate
        )
        db.add(db_volunteer)
        db.commit()
        db.refresh(db_volunteer)
        return db_volunteer
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating volunteer: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create volunteer: {str(e)}")

def get_volunteer(db: Session, volunteer_id: int) -> VolunteerResponse:
    volunteer = db.query(Volunteer).filter(Volunteer.id == volunteer_id).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    return volunteer

def get_volunteers(db: Session, skip: int = 0, limit: int = 100) -> list[VolunteerResponse]:
    return db.query(Volunteer).offset(skip).limit(limit).all()

def update_volunteer(db: Session, volunteer_id: int, volunteer_update: VolunteerUpdate, current_user: dict) -> VolunteerResponse:
    if current_user["type"] not in ["ong", "staff"]:
        raise HTTPException(status_code=403, detail="Permission denied")

    volunteer = db.query(Volunteer).filter(Volunteer.id == volunteer_id).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")

    update_data = volunteer_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(volunteer, key, value)

    db.commit()
    db.refresh(volunteer)
    return volunteer

def delete_volunteer(db: Session, volunteer_id: int, current_user: dict) -> dict:
    if current_user["type"] not in ["ong", "staff"]:
        raise HTTPException(status_code=403, detail="Permission denied")

    volunteer = db.query(Volunteer).filter(Volunteer.id == volunteer_id).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")

    db.delete(volunteer)
    db.commit()
    return {"detail": "Volunteer deleted"}