import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any, List
import logging
import base64

load_dotenv()

logger = logging.getLogger(__name__)

class PagarMeRecipientsAPI:
    BASE_URL = "https://api.pagar.me/core/v5"
    API_KEY = os.getenv("PAGARME_API_KEY")

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        """Retorna headers comuns para chamadas à API."""
        return {
            "Authorization": f"Basic {base64.b64encode(f'{PagarMeRecipientsAPI.API_KEY}:'.encode()).decode()}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def create_recipient(data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um recebedor na Pagar.me."""
        url = f"{PagarMeRecipientsAPI.BASE_URL}/recipients"
        headers = PagarMeRecipientsAPI._get_headers()
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me recipient created: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to create Pagar.me recipient: {e.response.json()}")
            raise Exception(f"Failed to create Pagar.me recipient: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error creating Pagar.me recipient: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def list_recipients(params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Lista todos os recebedores."""
        url = f"{PagarMeRecipientsAPI.BASE_URL}/recipients"
        headers = PagarMeRecipientsAPI._get_headers()
        try:
            response = requests.get(url, params=params or {}, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me recipients listed: {response.json()}")
            return response.json().get("data", [])
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to list Pagar.me recipients: {e.response.json()}")
            raise Exception(f"Failed to list Pagar.me recipients: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error listing Pagar.me recipients: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def get_recipient(recipient_id: str) -> Dict[str, Any]:
        """Obtém detalhes de um recebedor específico."""
        url = f"{PagarMeRecipientsAPI.BASE_URL}/recipients/{recipient_id}"
        headers = PagarMeRecipientsAPI._get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me recipient retrieved: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to get Pagar.me recipient: {e.response.json()}")
            raise Exception(f"Failed to get Pagar.me recipient: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error getting Pagar.me recipient: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def update_recipient(recipient_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um recebedor existente."""
        url = f"{PagarMeRecipientsAPI.BASE_URL}/recipients/{recipient_id}"
        headers = PagarMeRecipientsAPI._get_headers()
        try:
            response = requests.patch(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me recipient updated: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to update Pagar.me recipient: {e.response.json()}")
            raise Exception(f"Failed to update Pagar.me recipient: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error updating Pagar.me recipient: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")