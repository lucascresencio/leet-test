import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any, List
import logging
import base64

load_dotenv()

logger = logging.getLogger(__name__)

class PagarMeTransfersAPI:
    BASE_URL = "https://api.pagar.me/core/v5"
    API_KEY = os.getenv("PAGARME_API_KEY")

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        """Retorna headers comuns para chamadas à API."""
        return {
            "Authorization": f"Basic {base64.b64encode(f'{PagarMeTransfersAPI.API_KEY}:'.encode()).decode()}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def create_transfer(data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria uma transferência na Pagar.me."""
        url = f"{PagarMeTransfersAPI.BASE_URL}/transfers"
        headers = PagarMeTransfersAPI._get_headers()
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me transfer created: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to create Pagar.me transfer: {e.response.json()}")
            raise Exception(f"Failed to create Pagar.me transfer: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error creating Pagar.me transfer: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def list_transfers(params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Lista todas as transferências."""
        url = f"{PagarMeTransfersAPI.BASE_URL}/transfers"
        headers = PagarMeTransfersAPI._get_headers()
        try:
            response = requests.get(url, params=params or {}, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me transfers listed: {response.json()}")
            return response.json().get("data", [])
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to list Pagar.me transfers: {e.response.json()}")
            raise Exception(f"Failed to list Pagar.me transfers: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error listing Pagar.me transfers: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def get_transfer(transfer_id: str) -> Dict[str, Any]:
        """Obtém detalhes de uma transferência específica."""
        url = f"{PagarMeTransfersAPI.BASE_URL}/transfers/{transfer_id}"
        headers = PagarMeTransfersAPI._get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me transfer retrieved: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to get Pagar.me transfer: {e.response.json()}")
            raise Exception(f"Failed to get Pagar.me transfer: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error getting Pagar.me transfer: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def cancel_transfer(transfer_id: str) -> Dict[str, Any]:
        """Cancela uma transferência."""
        url = f"{PagarMeTransfersAPI.BASE_URL}/transfers/{transfer_id}/cancel"
        headers = PagarMeTransfersAPI._get_headers()
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me transfer canceled: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to cancel Pagar.me transfer: {e.response.json()}")
            raise Exception(f"Failed to cancel Pagar.me transfer: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error canceling Pagar.me transfer: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")