from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.payment import PaymentRequest, PaymentResponse
from app.services.payment_service import PaymentService
from app.config.database import get_db
import logging

router = APIRouter(prefix="/payments", tags=["Payments"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=PaymentResponse)
def create_payment(
    payment_data: PaymentRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends()
):
    """Cria um pagamento avulso."""
    try:
        transaction = PaymentService.create_payment(db, user_id, payment_data)
        return transaction
    except HTTPException as e:
        raise
    except Exception as e:
        logger.error(f"Error creating payment: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")