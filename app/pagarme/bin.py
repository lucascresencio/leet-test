import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any
import logging
import base64

load_dotenv()

logger = logging.getLogger(__name__)

class PagarMeBinAPI:
    BASE_URL = "https://api.pagar.me/core/v5"
    API_KEY = os.getenv("PAGARME_API_KEY")

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        """Retorna headers comuns para chamadas à API."""
        return {
            "Authorization": f"Basic {base64.b64encode(f'{PagarMeBinAPI.API_KEY}:'.encode()).decode()}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def get_bin(bin_number: str) -> Dict[str, Any]:
        """Obtém informações de um bin."""
        url = f"{PagarMeBinAPI.BASE_URL}/bins/{bin_number}"
        headers = PagarMeBinAPI._get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me bin retrieved: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to get Pagar.me bin: {e.response.json()}")
            raise Exception(f"Failed to get Pagar.me bin: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error getting Pagar.me bin: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")