import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any
import logging
import base64

load_dotenv()

logger = logging.getLogger(__name__)

class PagarMeRecurringSplitsAPI:
    BASE_URL = "https://api.pagar.me/core/v5"
    API_KEY = os.getenv("PAGARME_API_KEY")

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        """Retorna headers comuns para chamadas à API."""
        return {
            "Authorization": f"Basic {base64.b64encode(f'{PagarMeRecurringSplitsAPI.API_KEY}:'.encode()).decode()}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def create_recurring_split(subscription_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um split de recorrência na Pagar.me."""
        url = f"{PagarMeRecurringSplitsAPI.BASE_URL}/subscriptions/{subscription_id}/split"
        headers = PagarMeRecurringSplitsAPI._get_headers()
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me recurring split created: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to create Pagar.me recurring split: {e.response.json()}")
            raise Exception(f"Failed to create Pagar.me recurring split: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error creating Pagar.me recurring split: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def get_recurring_split(subscription_id: str) -> Dict[str, Any]:
        """Obtém detalhes de um split de recorrência."""
        url = f"{PagarMeRecurringSplitsAPI.BASE_URL}/subscriptions/{subscription_id}/split"
        headers = PagarMeRecurringSplitsAPI._get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me recurring split retrieved: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to get Pagar.me recurring split: {e.response.json()}")
            raise Exception(f"Failed to get Pagar.me recurring split: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error getting Pagar.me recurring split: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def update_recurring_split(subscription_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um split de recorrência."""
        url = f"{PagarMeRecurringSplitsAPI.BASE_URL}/subscriptions/{subscription_id}/split"
        headers = PagarMeRecurringSplitsAPI._get_headers()
        try:
            response = requests.patch(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me recurring split updated: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to update Pagar.me recurring split: {e.response.json()}")
            raise Exception(f"Failed to update Pagar.me recurring split: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error updating Pagar.me recurring split: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")