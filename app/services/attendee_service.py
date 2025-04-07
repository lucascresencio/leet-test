import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.attendee import Attendee
from app.models.address import Address
from app.schemas.attendee import AttendeeCreate, AttendeeUpdate, AttendeeResponse

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

def create_attendee(db: Session, attendee: AttendeeCreate, current_user: dict) -> Attendee:
    if current_user["type"] not in ["ong", "staff"]:
        raise HTTPException(status_code=403, detail="Permission denied")

    try:
        # Criar o endereço
        db_address = Address(**attendee.address.dict())
        db.add(db_address)
        db.flush()

        # Criar o attendee com o address_id
        db_attendee = Attendee(
            name=attendee.name,
            document=attendee.document,
            email=attendee.email,
            phone_number=attendee.phone_number,
            address_id=db_address.id
        )
        db.add(db_attendee)
        db.commit()
        db.refresh(db_attendee)
        return db_attendee
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating attendee: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create attendee: {str(e)}")

def get_attendee(db: Session, attendee_id: int) -> AttendeeResponse:
    attendee = db.query(Attendee).filter(Attendee.id == attendee_id).first()
    if not attendee:
        raise HTTPException(status_code=404, detail="Attendee not found")
    return attendee

def get_attendees(db: Session, skip: int = 0, limit: int = 100) -> list[AttendeeResponse]:
    return db.query(Attendee).offset(skip).limit(limit).all()

def update_attendee(db: Session, attendee_id: int, attendee_update: AttendeeUpdate, current_user: dict) -> AttendeeResponse:
    if current_user["type"] not in ["ong", "staff"]:
        raise HTTPException(status_code=403, detail="Permission denied")

    attendee = db.query(Attendee).filter(Attendee.id == attendee_id).first()
    if not attendee:
        raise HTTPException(status_code=404, detail="Attendee not found")

    update_data = attendee_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(attendee, key, value)

    db.commit()
    db.refresh(attendee)
    return attendee

def delete_attendee(db: Session, attendee_id: int, current_user: dict) -> dict:
    if current_user["type"] not in ["ong", "staff"]:
        raise HTTPException(status_code=403, detail="Permission denied")

    attendee = db.query(Attendee).filter(Attendee.id == attendee_id).first()
    if not attendee:
        raise HTTPException(status_code=404, detail="Attendee not found")

    db.delete(attendee)
    db.commit()
    return {"detail": "Attendee deleted"}