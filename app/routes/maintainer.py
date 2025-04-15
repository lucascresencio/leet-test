from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.maintainer import MaintainerCreate, MaintainerResponse, MaintainerBase
from app.schemas.address import AddressCreate, AddressResponse
from app.services.maintainer_service import create_maintainer, get_maintainers, get_maintainer_by_id
from app.services.auth_service import get_current_user
from app.config.database import get_db
from ..models.maintainer import Maintainer
from ..models.user import User
from sqlalchemy.orm import joinedload

from ..schemas.user import UserResponse

router = APIRouter(prefix="/maintainers", tags=["maintainers"])

@router.post("/create", response_model=MaintainerResponse)
def create_new_maintainer(
    maintainer: MaintainerCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_maintainer = create_maintainer(db, maintainer, current_user)

    return db_maintainer

# Rota para listar Mantenedores (protegida por token)
@router.get("/filter/", response_model=list[MaintainerResponse])
def get_maintainers_endpoint(
        status: Optional[str] = None,
        username: Optional[str] = None,
        name: Optional[str] = None,
        document: Optional[str] = None,
        email: Optional[str] = None,
        phone_number: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    return get_maintainers(db, current_user, status, username, name,
                           document, email, phone_number, skip, limit)

@router.get("/{maintainer_id}", response_model=MaintainerResponse)
def get_maintainer_by_id_endpoint(
    maintainer_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return get_maintainer_by_id(db, maintainer_id, current_user)