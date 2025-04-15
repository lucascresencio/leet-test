import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any, List
import logging
import base64

load_dotenv()

logger = logging.getLogger(__name__)

class PagarMeChargesAPI:
    BASE_URL = "https://api.pagar.me/core/v5"
    API_KEY = os.getenv("PAGARME_API_KEY")

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        """Retorna headers comuns para chamadas à API."""
        return {
            "Authorization": f"Basic {base64.b64encode(f'{PagarMeChargesAPI.API_KEY}:'.encode()).decode()}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def list_charges(params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Lista todas as cobranças."""
        url = f"{PagarMeChargesAPI.BASE_URL}/charges"
        headers = PagarMeChargesAPI._get_headers()
        try:
            response = requests.get(url, params=params or {}, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me charges listed: {response.json()}")
            return response.json().get("data", [])
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to list Pagar.me charges: {e.response.json()}")
            raise Exception(f"Failed to list Pagar.me charges: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error listing Pagar.me charges: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def get_charge(charge_id: str) -> Dict[str, Any]:
        """Obtém detalhes de uma cobrança específica."""
        url = f"{PagarMeChargesAPI.BASE_URL}/charges/{charge_id}"
        headers = PagarMeChargesAPI._get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me charge retrieved: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to get Pagar.me charge: {e.response.json()}")
            raise Exception(f"Failed to get Pagar.me charge: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error getting Pagar.me charge: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def update_charge_card(charge_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza o cartão de uma cobrança."""
        url = f"{PagarMeChargesAPI.BASE_URL}/charges/{charge_id}/card"
        headers = PagarMeChargesAPI._get_headers()
        try:
            response = requests.patch(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me charge card updated: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to update Pagar.me charge card: {e.response.json()}")
            raise Exception(f"Failed to update Pagar.me charge card: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error updating Pagar.me charge card: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def update_charge_due_date(charge_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza a data de vencimento de uma cobrança."""
        url = f"{PagarMeChargesAPI.BASE_URL}/charges/{charge_id}/due-date"
        headers = PagarMeChargesAPI._get_headers()
        try:
            response = requests.patch(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me charge due date updated: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to update Pagar.me charge due date: {e.response.json()}")
            raise Exception(f"Failed to update Pagar.me charge due date: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error updating Pagar.me charge due date: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def capture_charge(charge_id: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Captura uma cobrança."""
        url = f"{PagarMeChargesAPI.BASE_URL}/charges/{charge_id}/capture"
        headers = PagarMeChargesAPI._get_headers()
        try:
            response = requests.post(url, json=data or {}, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me charge captured: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to capture Pagar.me charge: {e.response.json()}")
            raise Exception(f"Failed to capture Pagar.me charge: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error capturing Pagar.me charge: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def retry_charge(charge_id: str) -> Dict[str, Any]:
        """Tenta novamente uma cobrança."""
        url = f"{PagarMeChargesAPI.BASE_URL}/charges/{charge_id}/retry"
        headers = PagarMeChargesAPI._get_headers()
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me charge retried: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to retry Pagar.me charge: {e.response.json()}")
            raise Exception(f"Failed to retry Pagar.me charge: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error retrying Pagar.me charge: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def cancel_charge(charge_id: str) -> Dict[str, Any]:
        """Cancela uma cobrança."""
        url = f"{PagarMeChargesAPI.BASE_URL}/charges/{charge_id}/cancel"
        headers = PagarMeChargesAPI._get_headers()
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me charge canceled: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to cancel Pagar.me charge: {e.response.json()}")
            raise Exception(f"Failed to cancel Pagar.me charge: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error canceling Pagar.me charge: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")