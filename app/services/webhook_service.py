import logging
from sqlalchemy.orm import Session
from app.models.transaction import Transaction, TransactionStatus
from app.models.webhook_log import WebhookLog
from typing import Dict, Any

logger = logging.getLogger(__name__)


class WebhookService:
    @staticmethod
    def handle_pagarme_webhook(db: Session, payload: Dict[str, Any]) -> None:
        """Processa notificações da Pagar.me."""
        event = payload.get("type")
        data = payload.get("data", {})

        webhook_log = WebhookLog(event=event, payload=payload)
        db.add(webhook_log)
        db.flush()

        try:
            if event.startswith("order."):
                order_id = data.get("id")
                transaction = db.query(Transaction).filter(Transaction.order_id == order_id).first()
                if not transaction:
                    logger.warning(f"No transaction found for order_id={order_id}")
                    return

                status_map = {
                    "pending": TransactionStatus.PENDING,
                    "paid": TransactionStatus.PAID,
                    "canceled": TransactionStatus.CANCELED,
                    "failed": TransactionStatus.FAILED,
                    "expired": TransactionStatus.EXPIRED
                }
                pagarme_status = data.get("status")
                new_status = status_map.get(pagarme_status)

                if new_status:
                    transaction.status = new_status
                    if new_status == TransactionStatus.FAILED:
                        transaction.error_message = data.get("last_transaction", {}).get("refuse_reason",
                                                                                         "Unknown error")
                    db.commit()
                    logger.info(f"Updated transaction {transaction.id} to status {new_status}")
                else:
                    logger.warning(f"Unknown Pagar.me status: {pagarme_status}")

        except Exception as e:
            db.rollback()
            logger.error(f"Error processing webhook {event}: {str(e)}")
            raise