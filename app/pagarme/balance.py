import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any
import logging
import base64

load_dotenv()

logger = logging.getLogger(__name__)

class PagarMeBalanceAPI:
    BASE_URL = "https://api.pagar.me/core/v5"
    API_KEY = os.getenv("PAGARME_API_KEY")

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        """Retorna headers comuns para chamadas à API."""
        return {
            "Authorization": f"Basic {base64.b64encode(f'{PagarMeBalanceAPI.API_KEY}:'.encode()).decode()}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def get_balance(recipient_id: str) -> Dict[str, Any]:
        """Obtém o saldo de um recebedor."""
        url = f"{PagarMeBalanceAPI.BASE_URL}/recipients/{recipient_id}/balance"
        headers = PagarMeBalanceAPI._get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me balance retrieved: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to get Pagar.me balance: {e.response.json()}")
            raise Exception(f"Failed to get Pagar.me balance: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error getting Pagar.me balance: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")