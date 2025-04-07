import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.campaign import Campaign, CampaignPhoto
from app.schemas.campaign import CampaignCreate, CampaignUpdate, CampaignResponse, CampaignPhotoResponse

# Configuração explícita do logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


def create_campaign(db: Session, campaign: CampaignCreate, current_user: dict) -> CampaignResponse:
    if current_user["type"] not in ["admin", "ong", "staff"]:
        logger.error(f"Permission denied for user type: {current_user['type']}")
        raise HTTPException(status_code=403, detail="Permission denied: only ONG or Staff can create campaigns")

    try:
        logger.debug(f"Dados recebidos no schema CampaignCreate: {campaign.dict()}")

        # Criar campanha
        db_campaign = Campaign()
        db_campaign.base_id = campaign.base_id
        db_campaign.ong_id = campaign.ong_id
        db_campaign.main_photo = campaign.main_photo
        db_campaign.title = campaign.title
        db_campaign.description = campaign.description
        db_campaign.goal = campaign.goal
        db_campaign.status = "I"

        logger.debug(f"Valores atribuídos ao db_campaign antes de adicionar: {vars(db_campaign)}")
        db.add(db_campaign)
        db.flush()
        logger.debug(f"Campaign created with id: {db_campaign.id}, valores após flush: {vars(db_campaign)}")

        # Adicionar fotos
        for photo_url in campaign.photo_urls:
            db_photo = CampaignPhoto(campaign_id=db_campaign.id, photo_url=photo_url)
            db.add(db_photo)
            logger.debug(f"Photo added: {photo_url}")

        db.commit()
        db.refresh(db_campaign)
        logger.debug(f"Campaign {db_campaign.id} committed successfully, valores finais: {vars(db_campaign)}")

        # Construir resposta
        return CampaignResponse(
            id=db_campaign.id,
            base_id=db_campaign.base_id,
            ong_id=db_campaign.ong_id,
            main_photo=db_campaign.main_photo,
            title=db_campaign.title,
            description=db_campaign.description,
            goal=db_campaign.goal,
            status=db_campaign.status,
            created_at=db_campaign.created_at,
            updated_at=db_campaign.updated_at,
            photos=[CampaignPhotoResponse.from_orm(photo) for photo in db_campaign.photos]
        )

    except Exception as e:
        db.rollback()
        logger.error(f"Error creating campaign: {str(e)}")
        raise HTTPException(statusABI_code=500, detail=f"Failed to create campaign: {str(e)}")


def get_campaign(db: Session, campaign_id: int) -> CampaignResponse:
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id, Campaign.status != "E").first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found or excluded")

    return CampaignResponse(
        id=campaign.id,
        base_id=campaign.base_id,
        ong_id=campaign.ong_id,
        main_photo=campaign.main_photo,
        title=campaign.title,
        description=campaign.description,
        goal=campaign.goal,
        status=campaign.status,
        created_at=campaign.created_at,
        updated_at=campaign.updated_at,
        photos=[CampaignPhotoResponse.from_orm(photo) for photo in campaign.photos]
    )


def get_campaigns(db: Session, skip: int = 0, limit: int = 100) -> list[CampaignResponse]:
    campaigns = db.query(Campaign).filter(Campaign.status != "E").offset(skip).limit(limit).all()
    return [
        CampaignResponse(
            id=c.id,
            base_id=c.base_id,
            ong_id=c.ong_id,
            main_photo=c.main_photo,
            title=c.title,
            description=c.description,
            goal=c.goal,
            status=c.status,
            created_at=c.created_at,
            updated_at=c.updated_at,
            photos=[CampaignPhotoResponse.from_orm(photo) for photo in c.photos]
        ) for c in campaigns
    ]


def update_campaign(db: Session, campaign_id: int, campaign_update: CampaignUpdate,
                    current_user: dict) -> CampaignResponse:
    if current_user["type"] not in ["admin", "ong", "staff"]:
        raise HTTPException(status_code=403, detail="Permission denied: only ONG or Staff can update campaigns")

    campaign = db.query(Campaign).filter(Campaign.id == campaign_id, Campaign.status != "E").first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found or excluded")

    update_data = campaign_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(campaign, key, value)
    campaign.status = "A"

    db.commit()
    db.refresh(campaign)
    return CampaignResponse(
        id=campaign.id,
        base_id=campaign.base_id,
        ong_id=campaign.ong_id,
        main_photo=campaign.main_photo,
        title=campaign.title,
        description=campaign.description,
        goal=campaign.goal,
        status=campaign.status,
        created_at=campaign.created_at,
        updated_at=campaign.updated_at,
        photos=[CampaignPhotoResponse.from_orm(photo) for photo in campaign.photos]
    )


def delete_campaign(db: Session, campaign_id: int, current_user: dict) -> CampaignResponse:
    if current_user["type"] not in ["ong", "staff"]:
        raise HTTPException(status_code=403, detail="Permission denied: only ONG or Staff can delete campaigns")

    campaign = db.query(Campaign).filter(Campaign.id == campaign_id, Campaign.status != "E").first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found or excluded")

    campaign.status = "E"
    db.commit()
    db.refresh(campaign)
    return CampaignResponse(
        id=campaign.id,
        base_id=campaign.base_id,
        ong_id=campaign.ong_id,
        main_photo=campaign.main_photo,
        title=campaign.title,
        description=campaign.description,
        goal=campaign.goal,
        status=campaign.status,
        created_at=campaign.created_at,
        updated_at=campaign.updated_at,
        photos=[CampaignPhotoResponse.from_orm(photo) for photo in campaign.photos]
    )