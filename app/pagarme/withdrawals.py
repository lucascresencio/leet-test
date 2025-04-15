import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any, List
import logging
import base64

load_dotenv()

logger = logging.getLogger(__name__)

class PagarMeWithdrawalsAPI:
    BASE_URL = "https://api.pagar.me/core/v5"
    API_KEY = os.getenv("PAGARME_API_KEY")

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        """Retorna headers comuns para chamadas à API."""
        return {
            "Authorization": f"Basic {base64.b64encode(f'{PagarMeWithdrawalsAPI.API_KEY}:'.encode()).decode()}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def create_withdrawal(recipient_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um saque na Pagar.me."""
        url = f"{PagarMeWithdrawalsAPI.BASE_URL}/recipients/{recipient_id}/withdrawals"
        headers = PagarMeWithdrawalsAPI._get_headers()
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me withdrawal created: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to create Pagar.me withdrawal: {e.response.json()}")
            raise Exception(f"Failed to create Pagar.me withdrawal: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error creating Pagar.me withdrawal: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def list_withdrawals(recipient_id: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Lista saques de um recebedor."""
        url = f"{PagarMeWithdrawalsAPI.BASE_URL}/recipients/{recipient_id}/withdrawals"
        headers = PagarMeWithdrawalsAPI._get_headers()
        try:
            response = requests.get(url, params=params or {}, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me withdrawals listed: {response.json()}")
            return response.json().get("data", [])
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to list Pagar.me withdrawals: {e.response.json()}")
            raise Exception(f"Failed to list Pagar.me withdrawals: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error listing Pagar.me withdrawals: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def get_withdrawal(recipient_id: str, withdrawal_id: str) -> Dict[str, Any]:
        """Obtém detalhes de um saque específico."""
        url = f"{PagarMeWithdrawalsAPI.BASE_URL}/recipients/{recipient_id}/withdrawals/{withdrawal_id}"
        headers = PagarMeWithdrawalsAPI._get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me withdrawal retrieved: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to get Pagar.me withdrawal: {e.response.json()}")
            raise Exception(f"Failed to get Pagar.me withdrawal: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error getting Pagar.me withdrawal: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")