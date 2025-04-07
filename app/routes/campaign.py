from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.campaign import CampaignCreate, CampaignUpdate, CampaignResponse
from app.services.campaign_service import create_campaign, get_campaign, get_campaigns, update_campaign, delete_campaign
from app.config.database import get_db
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/campaigns", tags=["campaigns"])

@router.post("/create", response_model=CampaignResponse)
def create_campaign_endpoint(campaign: CampaignCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return create_campaign(db, campaign, current_user)

@router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign_endpoint(campaign_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return get_campaign(db, campaign_id)

@router.get("/filter/", response_model=List[CampaignResponse])
def get_campaigns_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return get_campaigns(db, skip, limit)

@router.put("/{campaign_id}", response_model=CampaignResponse)
def update_campaign_endpoint(campaign_id: int, campaign: CampaignUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return update_campaign(db, campaign_id, campaign, current_user)

@router.delete("/{campaign_id}", response_model=CampaignResponse)
def delete_campaign_endpoint(campaign_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return delete_campaign(db, campaign_id, current_user)