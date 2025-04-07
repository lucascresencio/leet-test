from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, DateTime, UniqueConstraint, Date
from sqlalchemy.orm import relationship
from app.config.database import Base
from datetime import datetime

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    ong_id = Column(Integer, ForeignKey("ongs.id"), nullable=False)
    address_id = Column(Integer, ForeignKey("address.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    target_audience = Column(String(20), nullable=False)
    main_photo = Column(String)
    responsible_staff_id = Column(Integer, ForeignKey("staff.id"), nullable=True)
    status = Column(String(1), nullable=False, default="I")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("target_audience IN ('people', 'animals', 'both')", name="check_target_audience"),
        CheckConstraint("status IN ('I', 'A', 'E')", name="check_status"),
    )

    ong = relationship("ONG", back_populates="projects")
    address = relationship("Address")
    responsible_staff = relationship("Staff")
    photos = relationship("ProjectPhoto", back_populates="project")
    project_attendees = relationship("ProjectAttendee", back_populates="project")
    project_volunteers = relationship("ProjectVolunteer", back_populates="project")

class ProjectPhoto(Base):
    __tablename__ = "project_photos"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    photo_url = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="photos")


class ProjectAttendee(Base):
    __tablename__ = "project_attendees"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    attendee_id = Column(Integer, ForeignKey("attendees.id"), nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint("project_id", "attendee_id", name="unique_project_attendee"),)

    project = relationship("Project", back_populates="project_attendees")
    attendee = relationship("Attendee", back_populates="projects")

class ProjectVolunteer(Base):
    __tablename__ = "project_volunteers"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    volunteer_id = Column(Integer, ForeignKey("volunteers.id"), nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint("project_id", "volunteer_id", name="unique_project_volunteer"),)

    project = relationship("Project", back_populates="project_volunteers")
    volunteer = relationship("Volunteer", back_populates="projects")