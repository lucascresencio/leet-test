import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any, List
import logging
import base64

load_dotenv()

logger = logging.getLogger(__name__)

class PagarMeCyclesAPI:
    BASE_URL = "https://api.pagar.me/core/v5"
    API_KEY = os.getenv("PAGARME_API_KEY")

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        """Retorna headers comuns para chamadas à API."""
        return {
            "Authorization": f"Basic {base64.b64encode(f'{PagarMeCyclesAPI.API_KEY}:'.encode()).decode()}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def list_cycles(subscription_id: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Lista ciclos de uma assinatura."""
        url = f"{PagarMeCyclesAPI.BASE_URL}/subscriptions/{subscription_id}/cycles"
        headers = PagarMeCyclesAPI._get_headers()
        try:
            response = requests.get(url, params=params or {}, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me cycles listed: {response.json()}")
            return response.json().get("data", [])
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to list Pagar.me cycles: {e.response.json()}")
            raise Exception(f"Failed to list Pagar.me cycles: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error listing Pagar.me cycles: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def get_cycle(subscription_id: str, cycle_id: str) -> Dict[str, Any]:
        """Obtém detalhes de um ciclo específico."""
        url = f"{PagarMeCyclesAPI.BASE_URL}/subscriptions/{subscription_id}/cycles/{cycle_id}"
        headers = PagarMeCyclesAPI._get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me cycle retrieved: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to get Pagar.me cycle: {e.response.json()}")
            raise Exception(f"Failed to get Pagar.me cycle: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error getting Pagar.me cycle: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")