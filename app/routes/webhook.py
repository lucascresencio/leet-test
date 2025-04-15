from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.webhook_service import WebhookService
from app.config.database import get_db
from typing import Dict, Any
import logging

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])
logger = logging.getLogger(__name__)

@router.post("/pagarme")
def receive_pagarme_webhook(payload: Dict[str, Any], db: Session = Depends(get_db)):
    """Recebe notificações da Pagar.me."""
    try:
        WebhookService.handle_pagarme_webhook(db, payload)
        return {"status": "received"}
    except Exception as e:
        logger.error(f"Error processing Pagar.me webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")