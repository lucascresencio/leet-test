from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.maintainer import MaintainerCreate, MaintainerResponse, MaintainerBase
from app.schemas.address import AddressCreate
from app.services.maintainer_service import create_maintainer
from app.services.auth_service import get_current_user
from app.config.database import get_db
from ..models.user import User

router = APIRouter(prefix="/maintainers", tags=["maintainers"])

@router.post("/create", response_model=MaintainerResponse)
def create_new_maintainer(
    maintainer: MaintainerCreate,
    address: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # requires bearer token
):
    return create_maintainer(db, maintainer, address)

# Rota para listar Mantenedores (protegida por token)
@router.get("/list/", response_model=list[MaintainerResponse])
def maintainers_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # requires bearer token
):
    return db.query(MaintainerBase).all()