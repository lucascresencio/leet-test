from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.maintainer import Maintainer
from app.models.ong import ONG, OngMaintainer
from app.models.address import Address
from app.schemas.maintainer import MaintainerCreate, MaintainerResponse
from app.services.auth_service import get_password_hash, get_current_user
from ..config.pagarme import configure_pagarme
from ..models.staff import Staff
from ..models.user import User, UserType
from ..pagarme.address import PagarMeAddressAPI
from ..pagarme.customers import PagarMeCustomerAPI
from ..schemas.address import AddressResponse
import logging
import re

from ..schemas.user import UserResponse

# Configuração explícita do logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


def format_phone_number(phone: str) -> str:
    """Formata o número de telefone para o padrão da Pagar.me (+DDD)."""
    phone = re.sub(r'\D', '', phone)  # Remove caracteres não numéricos
    if not phone.startswith('+'):
        # Assumir Brasil (+55) se não houver código de país
        if phone.startswith('55'):
            phone = f'+{phone}'
        else:
            phone = f'+55{phone}'
    # Validar o padrão
    if not re.match(r'^\+(?:[0-9] ?){6,14}[0-9]$', phone):
        raise ValueError(f"Invalid phone number format: {phone}")
    return phone

def create_maintainer(db: Session, maintainer: MaintainerCreate, current_user: dict,):
    logger.debug(f"Current user: {current_user}")
    logger.debug(f"Maintainer data: {maintainer.dict()}")

    # Verificar permissões
    if current_user["type"] not in ["ong", "staff"]:
        logger.error(f"Permission denied for user type: {current_user['type']}")
        raise HTTPException(status_code=403, detail="Permission denied: only ONG or Staff can create maintainers")

    try:
        # Create address
        db_address = Address(**maintainer.address.dict())
        db.add(db_address)
        db.flush()
        logger.debug(f"Address created with id: {db_address.id}")

        maintainer_type = db.query(UserType).filter(UserType.name == "maintainer").first()
        if not maintainer_type:
            logger.error("User type 'maintainer' not found")
            raise HTTPException(status_code=500, detail="User type 'maintainer' not found")

        # Create user for maintainer
        db_user = User(
            username=maintainer.user.username.lower(),
            password=get_password_hash(maintainer.user.password),
            user_type_id=maintainer_type.id,
            name=maintainer.user.name,
            document=maintainer.user.document,
            email=maintainer.user.email,
            phone_number=maintainer.user.phone_number,
            photo=maintainer.user.photo,  # Foto agora em User
            status="I"
        )
        db.add(db_user)
        db.flush()
        logger.debug(f"User created with id: {db_user.id}")

        # Create maintainer and associate do address and user
        db_maintainer = Maintainer(
            address_id=db_address.id,
            user_id=db_user.id,
            client_id=None,  # Será preenchido após criar o cliente na Pagar.me
            is_business=maintainer.is_business
        )
        db.add(db_maintainer)
        db.flush()
        logger.debug(f"Maintainer created with id: {db_maintainer.id}")

        # Verificar ONG
        ong = None
        if current_user["type"] == "ong":
            ong = db.query(ONG).filter(ONG.user_id == current_user["id"]).first()
            if not ong:
                logger.error(f"ONG not found for user_id: {current_user['id']}")
                raise HTTPException(status_code=400, detail="ONG not found for current user")
        elif current_user["type"] in ["admin", "staff"] and maintainer.ong_id:
            ong = db.query(ONG).filter(ONG.id == maintainer.ong_id).first()
            if not ong:
                logger.error(f"ONG not found for ong_id: {maintainer.ong_id}")
                raise HTTPException(status_code=404, detail=f"ONG with id {maintainer.ong_id} not found")
        else:
            raise HTTPException(status_code=400, detail="ong_id is mandatory for non-ONG users")

        # Criar relação na tabela ong_maintainer
        ong_maintainer = OngMaintainer(
            ong_id=ong.id,
            maintainer_id=db_maintainer.id
        )
        db.add(ong_maintainer)
        db.flush()
        logger.debug(f"OngMaintainer created with ong_id: {ong.id}, maintainer_id: {db_maintainer.id}")

        # Configurar Pagar.me
        configure_pagarme()

        # Criar cliente na Pagar.me
        try:
            formatted_phone = format_phone_number(db_user.phone_number)
            client_data = {
                "external_id": str(db_maintainer.id),
                "name": db_user.name or db_user.username,
                "email": db_user.email,
                "type": "individual",
                "country": "br",
                "phone_numbers": [formatted_phone],
                "documents": [
                    {
                        "type": "cpf",
                        "number": db_user.document
                    }
                ]
            }
            logger.debug(f"Sending client data to Pagar.me: {client_data}")
            client = PagarMeCustomerAPI.create_customer(client_data)
            db_maintainer.client_id = client["id"]
            logger.debug(f"Pagar.me client created: client_id={client['id']}")

            # Criar endereço na Pagar.me
            address_data = {
                "line_1": f"{db_address.street}, {db_address.street_number or ''}".strip(),
                "line_2": db_address.complementary or "",
                "zip_code": db_address.zip_code,
                "city": db_address.city,
                "state": db_address.state.lower(),
                "country": "br",
                "status": "active"
            }
            logger.debug(f"Sending address data to Pagar.me: {address_data}")
            PagarMeAddressAPI.create_address(client["id"], address_data)
            logger.debug(f"Pagar.me address created for client_id={client['id']}")

            db.commit()
        except ValueError as ve:
            logger.error(f"Phone number validation failed: {str(ve)}")
            db.rollback()
            raise HTTPException(status_code=400, detail=str(ve))
        except Exception as e:
            logger.error(f"Failed to create Pagar.me client or address: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to create Pagar.me client or address: {str(e)}")

        db.commit()

        db.refresh(db_address)
        db.refresh(db_user)
        db.refresh(db_maintainer)

        logger.debug(f"Created address: {db_address.__dict__}")
        logger.debug(f"Created user: {db_user.__dict__}")
        logger.debug(f"Created maintainer: {db_maintainer.__dict__}")
        if current_user["type"] == "ong":
            logger.debug(f"Created ong_maintainer relation: ong_id={ong.id}, maintainer_id={db_maintainer.id}")

        return MaintainerResponse(
            id=db_maintainer.id,
            client_id=db_maintainer.client_id,
            ong_id=ong.id,
            user=UserResponse(
                id=db_user.id,
                username=db_user.username,
                name=db_user.name,
                document=db_user.document,
                email=db_user.email,
                phone_number=db_user.phone_number,
                user_type=db_user.user_type.name,
                status=db_user.status,
                photo=db_user.photo
            ),
            address=AddressResponse(
                id=db_address.id,
                street=db_address.street,
                street_number=db_address.street_number,
                complementary=db_address.complementary,
                city=db_address.city,
                state=db_address.state,
                zip_code=db_address.zip_code
            )
        )

    except HTTPException as e:
        db.rollback()
        logger.error(f"Error creating maintainer: {e.detail}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error creating maintainer: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create maintainer: {str(e)}")


def get_maintainers(
    db: Session,
    current_user: dict,
    status: Optional[str] = None,
    username: Optional[str] = None,
    name: Optional[str] = None,
    document: Optional[str] = None,
    email: Optional[str] = None,
    phone_number: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> list[MaintainerResponse]:
    # Log para inspecionar current_user
    logger.debug(f"Current user: {current_user}")

    # Verificar permissão
    if current_user["type"] not in ["admin", "ong", "staff"]:
        logger.error(f"Permission denied for user type: {current_user['type']}")
        raise HTTPException(status_code=403, detail="Permission denied: only Admin, ONG, or Staff can list maintainers")

    # Começar a query com OngMaintainer
    query = db.query(OngMaintainer).join(Maintainer, OngMaintainer.maintainer_id == Maintainer.id).join(User, Maintainer.user_id == User.id)

    # Obter o ID do usuário de forma segura
    user_id = None
    if "user_id" in current_user:  # Caso ong
        user_id = current_user["user_id"]
    elif "user" in current_user and current_user["user"]:  # Caso staff ou maintainer
        user_id = current_user["user"].id
    # Caso "developer" (admin) não precisa de user_id, pois lista todos

    # Restringir ong_id para ong e staff
    if current_user["type"] == "ong":
        if not user_id:
            logger.error("No user_id found for ONG user")
            raise HTTPException(status_code=400, detail="Invalid user data: missing user_id")
        ong = db.query(ONG).filter(ONG.user_id == user_id).first()
        if not ong:
            logger.error(f"ONG not found for user_id: {user_id}")
            raise HTTPException(status_code=400, detail="ONG not found for current user")
        query = query.filter(OngMaintainer.ong_id == ong.id)
        logger.debug(f"Restricted to ong_id: {ong.id} for ONG user")
    elif current_user["type"] == "staff" and current_user["role"] != "admin":
        if not user_id:
            logger.error("No user_id found for Staff user")
            raise HTTPException(status_code=400, detail="Invalid user data: missing user_id")
        staff = db.query(Staff).filter(Staff.user_id == user_id).first()
        if not staff:
            logger.error(f"Staff not found for user_id: {user_id}")
            raise HTTPException(status_code=400, detail="Staff not associated with any ONG")
        query = query.filter(OngMaintainer.ong_id == staff.ong_id)
        logger.debug(f"Restricted to ong_id: {staff.ong_id} for Staff user")
    # Admin (incluindo "developer") pode listar todos, sem restrição

    # Aplicar filtros
    if status:
        query = query.filter(User.status == status)
        logger.debug(f"Filtro aplicado: status={status}")
    if username:
        query = query.filter(User.username.ilike(f"%{username}%"))
        logger.debug(f"Filtro aplicado: username={username}")
    if name:
        query = query.filter(User.name.ilike(f"%{name}%"))
        logger.debug(f"Filtro aplicado: name={name}")
    if document:
        query = query.filter(User.document.ilike(f"%{document}%"))
        logger.debug(f"Filtro aplicado: document={document}")
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
        logger.debug(f"Filtro aplicado: email={email}")
    if phone_number:
        query = query.filter(User.phone_number.ilike(f"%{phone_number}%"))
        logger.debug(f"Filtro aplicado: phone_number={phone_number}")

    maintainers = query.offset(skip).limit(limit).all()
    logger.debug(f"Query executada: {str(query)}, resultados: {len(maintainers)}")

    return [
        MaintainerResponse(
            id=maintainer.maintainer.id,
            ong_id=maintainer.ong_id,
            client_id=maintainer.maintainer.client_id,
            user=UserResponse(
                id=maintainer.maintainer.user.id,
                username=maintainer.maintainer.user.username,
                name=maintainer.maintainer.user.name,
                document=maintainer.maintainer.user.document,
                email=maintainer.maintainer.user.email,
                phone_number=maintainer.maintainer.user.phone_number,
                user_type=maintainer.maintainer.user.user_type.name,
                status=maintainer.maintainer.user.status,
                photo=maintainer.maintainer.user.photo
            ),
            address=AddressResponse(
                id=maintainer.maintainer.address.id,
                street=maintainer.maintainer.address.street,
                street_number=maintainer.maintainer.address.street_number,
                complementary=maintainer.maintainer.address.complementary,
                city=maintainer.maintainer.address.city,
                state=maintainer.maintainer.address.state,
                zip_code=maintainer.maintainer.address.zip_code
            )
        ) for maintainer in maintainers
    ]


def get_maintainer_by_id(db: Session, maintainer_id: int, current_user: dict) -> MaintainerResponse:
    logger.debug(f"Current user: {current_user}")

    # Verificar permissão básica
    if current_user["type"] not in ["admin", "ong", "staff"]:
        logger.error(f"Permission denied for user type: {current_user['type']}")
        raise HTTPException(status_code=403, detail="Permission denied: only Admin, ONG, or Staff can get maintainers")

    # Obter o ID do usuário de forma segura
    user_id = None
    if "user_id" in current_user:  # Caso ong
        user_id = current_user["user_id"]
    elif "user" in current_user and current_user["user"]:  # Caso staff ou maintainer
        user_id = current_user["user"].id
    # Admin (developer) não precisa de user_id

    # Construir a query com OngMaintainer como base
    query = db.query(OngMaintainer).join(Maintainer, OngMaintainer.maintainer_id == Maintainer.id).join(User, Maintainer.user_id == User.id)

    # Aplicar filtro pelo ID do maintainer (usando OngMaintainer.id)
    query = query.filter(OngMaintainer.id == maintainer_id)

    # Restringir ong_id para ong e staff
    if current_user["type"] == "ong":
        if not user_id:
            logger.error("No user_id found for ONG user")
            raise HTTPException(status_code=400, detail="Invalid user data: missing user_id")
        ong = db.query(ONG).filter(ONG.user_id == user_id).first()
        if not ong:
            logger.error(f"ONG not found for user_id: {user_id}")
            raise HTTPException(status_code=400, detail="ONG not found for current user")
        query = query.filter(OngMaintainer.ong_id == ong.id)
        logger.debug(f"Restricted to ong_id: {ong.id} for ONG user")
    elif current_user["type"] == "staff" and (current_user.get("role") != "admin"):  # Admin staff pode ver todos
        if not user_id:
            logger.error("No user_id found for Staff user")
            raise HTTPException(status_code=400, detail="Invalid user data: missing user_id")
        staff = db.query(Staff).filter(Staff.user_id == user_id).first()
        if not staff:
            logger.error(f"Staff not found for user_id: {user_id}")
            raise HTTPException(status_code=400, detail="Staff not associated with any ONG")
        query = query.filter(OngMaintainer.ong_id == staff.ong_id)
        logger.debug(f"Restricted to ong_id: {staff.ong_id} for Staff user")
    # Admin (incluindo "developer") pode acessar qualquer maintainer

    # Executar a query
    maintainer = query.first()
    if not maintainer:
        logger.debug(f"Maintainer not found for id: {maintainer_id}")
        raise HTTPException(status_code=404, detail="Maintainer not found")

    # Retornar o resultado
    return MaintainerResponse(
        id=maintainer.maintainer.id,
        ong_id=maintainer.ong_id,
        client_id=maintainer.maintainer.client_id,
        user=UserResponse(
            id=maintainer.maintainer.user.id,
            username=maintainer.maintainer.user.username,
            name=maintainer.maintainer.user.name,
            document=maintainer.maintainer.user.document,
            email=maintainer.maintainer.user.email,
            phone_number=maintainer.maintainer.user.phone_number,
            user_type=maintainer.maintainer.user.user_type.name,
            status=maintainer.maintainer.user.status,
            photo=maintainer.maintainer.user.photo
        ),
        address=AddressResponse(
            id=maintainer.maintainer.address.id,
            street=maintainer.maintainer.address.street,
            street_number=maintainer.maintainer.address.street_number,
            complementary=maintainer.maintainer.address.complementary,
            city=maintainer.maintainer.address.city,
            state=maintainer.maintainer.address.state,
            zip_code=maintainer.maintainer.address.zip_code
        )
    )