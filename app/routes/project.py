from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.services.project_service import create_project, get_project, get_projects, update_project, delete_project
from app.config.database import get_db
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/create", response_model=ProjectResponse)
def create_project_endpoint(project: ProjectCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return create_project(db, project, current_user)

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project_endpoint(project_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return get_project(db, project_id)

@router.get("/filter/", response_model=List[ProjectResponse])
def get_projects_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return get_projects(db, skip, limit)

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project_endpoint(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return update_project(db, project_id, project, current_user)

@router.delete("/{project_id}", response_model=ProjectResponse)
def delete_project_endpoint(project_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return delete_project(db, project_id, current_user)