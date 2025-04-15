import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any, List
import logging
import base64

load_dotenv()

logger = logging.getLogger(__name__)

class PagarMeInvoicesAPI:
    BASE_URL = "https://api.pagar.me/core/v5"
    API_KEY = os.getenv("PAGARME_API_KEY")

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        """Retorna headers comuns para chamadas à API."""
        return {
            "Authorization": f"Basic {base64.b64encode(f'{PagarMeInvoicesAPI.API_KEY}:'.encode()).decode()}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def list_invoices(subscription_id: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Lista faturas de uma assinatura."""
        url = f"{PagarMeInvoicesAPI.BASE_URL}/subscriptions/{subscription_id}/invoices"
        headers = PagarMeInvoicesAPI._get_headers()
        try:
            response = requests.get(url, params=params or {}, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me invoices listed: {response.json()}")
            return response.json().get("data", [])
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to list Pagar.me invoices: {e.response.json()}")
            raise Exception(f"Failed to list Pagar.me invoices: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error listing Pagar.me invoices: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def get_invoice(subscription_id: str, invoice_id: str) -> Dict[str, Any]:
        """Obtém detalhes de uma fatura específica."""
        url = f"{PagarMeInvoicesAPI.BASE_URL}/subscriptions/{subscription_id}/invoices/{invoice_id}"
        headers = PagarMeInvoicesAPI._get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me invoice retrieved: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to get Pagar.me invoice: {e.response.json()}")
            raise Exception(f"Failed to get Pagar.me invoice: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error getting Pagar.me invoice: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")