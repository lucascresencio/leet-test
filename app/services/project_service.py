import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.project import Project, ProjectPhoto, ProjectAttendee, ProjectVolunteer
from app.models.attendee import Attendee
from app.models.volunteer import Volunteer
from app.models.address import Address
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

def create_project(db: Session, project: ProjectCreate, current_user: dict) -> Project:
    if current_user["type"] not in ["ong", "staff"]:
        raise HTTPException(status_code=403, detail="Permission denied")

    try:
        db_address = Address(**project.address.dict())
        db.add(db_address)
        db.flush()

        db_project = Project(
            ong_id=project.ong_id,
            address_id=db_address.id,
            title=project.title,
            description=project.description,
            target_audience=project.target_audience,
            responsible_staff_id=project.responsible_staff_id,
            main_photo=project.main_photo,
            status="I"
        )
        db.add(db_project)
        db.flush()

        for photo_url in project.photo_urls:
            db_photo = ProjectPhoto(project_id=db_project.id, photo_url=photo_url)
            db.add(db_photo)

        for attendee_id in project.attendee_ids:
            db_attendee = ProjectAttendee(project_id=db_project.id, attendee_id=attendee_id)
            db.add(db_attendee)

        for volunteer_id in project.volunteer_ids:
            db_volunteer = ProjectVolunteer(project_id=db_project.id, volunteer_id=volunteer_id)
            db.add(db_volunteer)

        db.commit()
        db.refresh(db_project)
        return db_project
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating project: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create project: {str(e)}")

def get_project(db: Session, project_id: int) -> ProjectResponse:
    project = db.query(Project).filter(Project.id == project_id, Project.status != "E").first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or excluded")
    return project

def get_projects(db: Session, skip: int = 0, limit: int = 100) -> list[ProjectResponse]:
    return db.query(Project).filter(Project.status != "E").offset(skip).limit(limit).all()

def update_project(db: Session, project_id: int, project_update: ProjectUpdate, current_user: dict) -> ProjectResponse:
    if current_user["type"] not in ["ong", "staff"]:
        raise HTTPException(status_code=403, detail="Permission denied")

    project = db.query(Project).filter(Project.id == project_id, Project.status != "E").first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or excluded")

    update_data = project_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)
    project.status = "A"

    db.commit()
    db.refresh(project)
    return project

def delete_project(db: Session, project_id: int, current_user: dict) -> ProjectResponse:
    if current_user["type"] not in ["ong", "staff"]:
        raise HTTPException(status_code=403, detail="Permission denied")

    project = db.query(Project).filter(Project.id == project_id, Project.status != "E").first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or excluded")

    project.status = "E"
    db.commit()
    db.refresh(project)
    return project