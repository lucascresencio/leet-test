import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any, List
import logging
import base64

load_dotenv()

logger = logging.getLogger(__name__)

class PagarMeSubscriptionItemUsagesAPI:
    BASE_URL = "https://api.pagar.me/core/v5"
    API_KEY = os.getenv("PAGARME_API_KEY")

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        """Retorna headers comuns para chamadas à API."""
        return {
            "Authorization": f"Basic {base64.b64encode(f'{PagarMeSubscriptionItemUsagesAPI.API_KEY}:'.encode()).decode()}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def create_usage(subscription_id: str, item_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um uso de item de assinatura na Pagar.me."""
        url = f"{PagarMeSubscriptionItemUsagesAPI.BASE_URL}/subscriptions/{subscription_id}/items/{item_id}/usages"
        headers = PagarMeSubscriptionItemUsagesAPI._get_headers()
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me usage created: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to create Pagar.me usage: {e.response.json()}")
            raise Exception(f"Failed to create Pagar.me usage: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error creating Pagar.me usage: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def list_usages(subscription_id: str, item_id: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Lista usos de um item de assinatura."""
        url = f"{PagarMeSubscriptionItemUsagesAPI.BASE_URL}/subscriptions/{subscription_id}/items/{item_id}/usages"
        headers = PagarMeSubscriptionItemUsagesAPI._get_headers()
        try:
            response = requests.get(url, params=params or {}, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me usages listed: {response.json()}")
            return response.json().get("data", [])
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to list Pagar.me usages: {e.response.json()}")
            raise Exception(f"Failed to list Pagar.me usages: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error listing Pagar.me usages: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def delete_usage(subscription_id: str, item_id: str, usage_id: str) -> None:
        """Exclui um uso de item de assinatura."""
        url = f"{PagarMeSubscriptionItemUsagesAPI.BASE_URL}/subscriptions/{subscription_id}/items/{item_id}/usages/{usage_id}"
        headers = PagarMeSubscriptionItemUsagesAPI._get_headers()
        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me usage deleted: subscription_id={subscription_id}, item_id={item_id}, usage_id={usage_id}")
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to delete Pagar.me usage: {e.response.json()}")
            raise Exception(f"Failed to delete Pagar.me usage: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error deleting Pagar.me usage: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")