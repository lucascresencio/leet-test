from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.maintainer import MaintainerCreate, MaintainerResponse, MaintainerBase
from app.schemas.address import AddressCreate, AddressResponse
from app.services.maintainer_service import create_maintainer, maintainers_list
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

    # Serialização manual dos sub-objetos
    user_response = UserResponse.from_orm(db_maintainer.user)
    address_response = AddressResponse.from_orm(db_maintainer.address)
    response = MaintainerResponse(
        id=db_maintainer.id,
        user_id=db_maintainer.user_id,
        address_id=db_maintainer.address_id,
        name=db_maintainer.name,
        user=user_response,
        address=address_response,
        is_business=db_maintainer.is_business
    )
    return response

# Rota para listar Mantenedores (protegida por token)
@router.get("/list/", response_model=list[MaintainerResponse])
def maintainers_list_all(
    db: Session = Depends(get_db),
):
    # Buscar todos os maintainers no banco
    maintainers = maintainers_list(db)

    return maintainers
