import logging
from typing import Dict, Any
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.transaction import Transaction, PaymentMethod, TransactionStatus
from app.models.maintainer import Maintainer
from app.models.ong import ONG
from app.models.campaign import Campaign
from app.models.base import Base
from app.models.project import Project
from app.models.attendee import Attendee
from app.models.card import Card
from app.pagarme.orders import PagarMeOrdersAPI
from app.pagarme.cards import PagarMeCardsAPI
from app.pagarme.charges import PagarMeChargesAPI
from app.pagarme.customers import PagarMeCustomerAPI
import os

logger = logging.getLogger(__name__)


class PaymentService:
    LEET_RECIPIENT_ID = os.getenv("LEET_RECIPIENT_ID")

    @staticmethod
    def create_payment(db: Session, user_id: int, payment_data: Dict[str, Any]) -> Transaction:
        """Cria um pagamento avulso."""
        # Verificar se o usuário é um mantenedor
        maintainer = db.query(Maintainer).filter(Maintainer.user_id == user_id).first()
        if not maintainer:
            logger.error(f"User {user_id} is not a maintainer")
            raise HTTPException(status_code=403, detail="Only maintainers can make payments")

        # Validar ONG
        ong = db.query(ONG).filter(ONG.id == payment_data.ong_id).first()
        if not ong:
            logger.error(f"ONG {payment_data.ong_id} not found")
            raise HTTPException(status_code=404, detail="ONG not found")

        # Validar destinos opcionais
        campaign = None
        base = None
        project = None
        attendee = None

        if payment_data.campaign_id:
            campaign = db.query(Campaign).filter(Campaign.id == payment_data.campaign_id,
                                                 Campaign.ong_id == ong.id).first()
            if not campaign:
                logger.error(f"Campaign {payment_data.campaign_id} not found or not associated with ONG {ong.id}")
                raise HTTPException(status_code=404, detail="Campaign not found or not associated with ONG")

        if payment_data.base_id:
            base = db.query(Base).filter(Base.id == payment_data.base_id, Base.ong_id == ong.id).first()
            if not base:
                logger.error(f"Base {payment_data.base_id} not found or not associated with ONG {ong.id}")
                raise HTTPException(status_code=404, detail="Base not found or not associated with ONG")

        if payment_data.project_id:
            project = db.query(Project).filter(Project.id == payment_data.project_id, Project.ong_id == ong.id).first()
            if not project:
                logger.error(f"Project {payment_data.project_id} not found or not associated with ONG {ong.id}")
                raise HTTPException(status_code=404, detail="Project not found or not associated with ONG")

        if payment_data.attendee_id:
            if not payment_data.project_id:
                logger.error("Attendee specified without project")
                raise HTTPException(status_code=400, detail="Project ID is required when specifying an attendee")
            attendee = db.query(Attendee).filter(
                Attendee.id == payment_data.attendee_id,
                Attendee.project_id == payment_data.project_id
            ).first()
            if not attendee:
                logger.error(
                    f"Attendee {payment_data.attendee_id} not found or not associated with project {payment_data.project_id}")
                raise HTTPException(status_code=404, detail="Attendee not found or not associated with project")

        # Calcular comissão
        commission_rate = ong.commission_rate
        commission_amount = payment_data.amount * commission_rate
        net_amount = payment_data.amount - commission_amount

        # Criar transação inicial
        transaction = Transaction(
            maintainer_id=maintainer.id,
            ong_id=ong.id,
            campaign_id=payment_data.campaign_id,
            base_id=payment_data.base_id,
            project_id=payment_data.project_id,
            attendee_id=payment_data.attendee_id,
            amount=payment_data.amount,
            commission_amount=commission_amount,
            payment_method=payment_data.payment_method,
            status=TransactionStatus.PENDING
        )
        db.add(transaction)
        db.flush()

        try:
            # Criar ou obter cliente na Pagar.me
            customer_data = {
                "name": maintainer.user.name,
                "email": maintainer.user.email,
                "type": "individual",
                "document": maintainer.user.document,
                "phones": {
                    "mobile_phone": {
                        "country_code": "+55",
                        "area_code": maintainer.user.phone_number[:2],
                        "number": maintainer.user.phone_number[2:]
                    }
                }
            }
            customer_response = PagarMeCustomerAPI.create_customer(customer_data)
            customer_id = customer_response["id"]

            # Preparar descrição do item
            description = f"Doação para ONG {ong.id}"
            if campaign:
                description += f", campanha {campaign.name}"
            elif base:
                description += f", base {base.name}"
            elif project:
                description += f", projeto {project.name}"
                if attendee:
                    description += f", participante {attendee.name}"

            # Preparar dados do pedido
            order_data = {
                "customer_id": customer_id,
                "items": [
                    {
                        "amount": int(payment_data.amount * 100),
                        "description": description,
                        "quantity": 1
                    }
                ],
                "payments": [
                    {
                        "payment_method": payment_data.payment_method,
                        "amount": int(payment_data.amount * 100),
                        "split": [
                            {
                                "amount": int(net_amount * 100),
                                "recipient_id": f"re_ong_{ong.id}",
                                "type": "flat"
                            },
                            {
                                "amount": int(commission_amount * 100),
                                "recipient_id": PaymentService.LEET_RECIPIENT_ID,
                                "type": "flat"
                            }
                        ]
                    }
                ]
            }

            # Lógica por método de pagamento
            if payment_data.payment_method == PaymentMethod.CREDIT_CARD:
                card_details = payment_data.card_details
                if not card_details:
                    raise HTTPException(status_code=400, detail="Card details required for credit card payment")

                if card_details.card_id:
                    transaction.card_id = card_details.card_id
                    order_data["payments"][0]["credit_card"] = {"card_id": card_details.card_id}
                else:
                    if not all([card_details.number, card_details.holder_name, card_details.expiration_date,
                                card_details.cvv]):
                        raise HTTPException(status_code=400, detail="Complete card details required")

                    card_data = {
                        "number": card_details.number,
                        "holder_name": card_details.holder_name,
                        "expiration_date": card_details.expiration_date,
                        "cvv": card_details.cvv
                    }
                    card_response = PagarMeCardsAPI.create_card(card_data)
                    card_id = card_response["id"]
                    transaction.card_id = card_id
                    order_data["payments"][0]["credit_card"] = {"card_id": card_id}

                    new_card = Card(
                        maintainer_id=maintainer.id,
                        card_id=card_id,
                        last_four_digits=card_response["last_four_digits"],
                        brand=card_response["brand"],
                        status="active"
                    )
                    db.add(new_card)

            elif payment_data.payment_method == PaymentMethod.BOLETO:
                order_data["payments"][0]["boleto"] = {
                    "instructions": "Pague até o vencimento para garantir a doação."
                }

            elif payment_data.payment_method == PaymentMethod.PIX:
                order_data["payments"][0]["pix"] = {
                    "expires_in": 3600
                }

            # Criar pedido na Pagar.me
            order_response = PagarMeOrdersAPI.create_order(order_data)
            transaction.order_id = order_response["id"]
            charge = order_response["charges"][0]
            transaction.charge_id = charge["id"]

            # Atualizar transação com detalhes
            if payment_data.payment_method == PaymentMethod.BOLETO:
                transaction.boleto_url = charge["last_transaction"]["url"]
                transaction.boleto_barcode = charge["last_transaction"]["barcode"]
            elif payment_data.payment_method == PaymentMethod.PIX:
                transaction.pix_qr_code = charge["last_transaction"]["qr_code_url"]
                transaction.pix_code = charge["last_transaction"]["qr_code"]

            transaction.status = TransactionStatus.PENDING
            if charge["status"] == "failed":
                transaction.status = TransactionStatus.FAILED
                transaction.error_message = charge["last_transaction"].get("refuse_reason", "Unknown error")
                raise HTTPException(status_code=400, detail=transaction.error_message)

            db.commit()
            logger.info(f"Payment created: transaction_id={transaction.id}, order_id={transaction.order_id}")
            return transaction

        except HTTPException:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to process payment: {str(e)}")
            error_message = str(e)
            if "expired" in error_message.lower():
                transaction.error_message = "Card expired"
                transaction.status = TransactionStatus.FAILED
                db.commit()
                raise HTTPException(status_code=400, detail="Card expired")
            transaction.error_message = error_message
            transaction.status = TransactionStatus.FAILED
            db.commit()
            raise HTTPException(status_code=500, detail=f"Payment processing failed: {error_message}")