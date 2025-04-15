import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any, List
import logging
import base64

load_dotenv()

logger = logging.getLogger(__name__)

class PagarMeSubscriptionsAPI:
    BASE_URL = "https://api.pagar.me/core/v5"
    API_KEY = os.getenv("PAGARME_API_KEY")

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        """Retorna headers comuns para chamadas à API."""
        return {
            "Authorization": f"Basic {base64.b64encode(f'{PagarMeSubscriptionsAPI.API_KEY}:'.encode()).decode()}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def create_subscription(data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria uma assinatura na Pagar.me."""
        url = f"{PagarMeSubscriptionsAPI.BASE_URL}/subscriptions"
        headers = PagarMeSubscriptionsAPI._get_headers()
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me subscription created: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to create Pagar.me subscription: {e.response.json()}")
            raise Exception(f"Failed to create Pagar.me subscription: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error creating Pagar.me subscription: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def list_subscriptions(params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Lista todas as assinaturas."""
        url = f"{PagarMeSubscriptionsAPI.BASE_URL}/subscriptions"
        headers = PagarMeSubscriptionsAPI._get_headers()
        try:
            response = requests.get(url, params=params or {}, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me subscriptions listed: {response.json()}")
            return response.json().get("data", [])
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to list Pagar.me subscriptions: {e.response.json()}")
            raise Exception(f"Failed to list Pagar.me subscriptions: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error listing Pagar.me subscriptions: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def get_subscription(subscription_id: str) -> Dict[str, Any]:
        """Obtém detalhes de uma assinatura específica."""
        url = f"{PagarMeSubscriptionsAPI.BASE_URL}/subscriptions/{subscription_id}"
        headers = PagarMeSubscriptionsAPI._get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me subscription retrieved: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to get Pagar.me subscription: {e.response.json()}")
            raise Exception(f"Failed to get Pagar.me subscription: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error getting Pagar.me subscription: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def update_subscription(subscription_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza uma assinatura existente."""
        url = f"{PagarMeSubscriptionsAPI.BASE_URL}/subscriptions/{subscription_id}"
        headers = PagarMeSubscriptionsAPI._get_headers()
        try:
            response = requests.patch(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me subscription updated: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to update Pagar.me subscription: {e.response.json()}")
            raise Exception(f"Failed to update Pagar.me subscription: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error updating Pagar.me subscription: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def update_subscription_card(subscription_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza o cartão de uma assinatura."""
        url = f"{PagarMeSubscriptionsAPI.BASE_URL}/subscriptions/{subscription_id}/card"
        headers = PagarMeSubscriptionsAPI._get_headers()
        try:
            response = requests.patch(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me subscription card updated: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to update Pagar.me subscription card: {e.response.json()}")
            raise Exception(f"Failed to update Pagar.me subscription card: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error updating Pagar.me subscription card: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def update_subscription_payment_method(subscription_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza o método de pagamento de uma assinatura."""
        url = f"{PagarMeSubscriptionsAPI.BASE_URL}/subscriptions/{subscription_id}/payment-method"
        headers = PagarMeSubscriptionsAPI._get_headers()
        try:
            response = requests.patch(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me subscription payment method updated: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to update Pagar.me subscription payment method: {e.response.json()}")
            raise Exception(f"Failed to update Pagar.me subscription payment method: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error updating Pagar.me subscription payment method: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def update_subscription_due_date(subscription_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza a data de vencimento de uma assinatura."""
        url = f"{PagarMeSubscriptionsAPI.BASE_URL}/subscriptions/{subscription_id}/due-date"
        headers = PagarMeSubscriptionsAPI._get_headers()
        try:
            response = requests.patch(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me subscription due date updated: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to update Pagar.me subscription due date: {e.response.json()}")
            raise Exception(f"Failed to update Pagar.me subscription due date: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error updating Pagar.me subscription due date: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def update_subscription_minimum_price(subscription_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza o preço mínimo de uma assinatura."""
        url = f"{PagarMeSubscriptionsAPI.BASE_URL}/subscriptions/{subscription_id}/minimum-price"
        headers = PagarMeSubscriptionsAPI._get_headers()
        try:
            response = requests.patch(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me subscription minimum price updated: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to update Pagar.me subscription minimum price: {e.response.json()}")
            raise Exception(f"Failed to update Pagar.me subscription minimum price: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error updating Pagar.me subscription minimum price: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def cancel_subscription(subscription_id: str) -> Dict[str, Any]:
        """Cancela uma assinatura."""
        url = f"{PagarMeSubscriptionsAPI.BASE_URL}/subscriptions/{subscription_id}/cancel"
        headers = PagarMeSubscriptionsAPI._get_headers()
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me subscription canceled: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to cancel Pagar.me subscription: {e.response.json()}")
            raise Exception(f"Failed to cancel Pagar.me subscription: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error canceling Pagar.me subscription: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")