import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any, List
import logging
import base64

load_dotenv()

logger = logging.getLogger(__name__)

class PagarMeBankAccountsAPI:
    BASE_URL = "https://api.pagar.me/core/v5"
    API_KEY = os.getenv("PAGARME_API_KEY")

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        """Retorna headers comuns para chamadas à API."""
        return {
            "Authorization": f"Basic {base64.b64encode(f'{PagarMeBankAccountsAPI.API_KEY}:'.encode()).decode()}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def create_bank_account(recipient_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria uma conta bancária na Pagar.me."""
        url = f"{PagarMeBankAccountsAPI.BASE_URL}/recipients/{recipient_id}/bank_accounts"
        headers = PagarMeBankAccountsAPI._get_headers()
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me bank account created: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to create Pagar.me bank account: {e.response.json()}")
            raise Exception(f"Failed to create Pagar.me bank account: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error creating Pagar.me bank account: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def list_bank_accounts(recipient_id: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Lista contas bancárias de um recebedor."""
        url = f"{PagarMeBankAccountsAPI.BASE_URL}/recipients/{recipient_id}/bank_accounts"
        headers = PagarMeBankAccountsAPI._get_headers()
        try:
            response = requests.get(url, params=params or {}, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me bank accounts listed: {response.json()}")
            return response.json().get("data", [])
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to list Pagar.me bank accounts: {e.response.json()}")
            raise Exception(f"Failed to list Pagar.me bank accounts: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error listing Pagar.me bank accounts: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def get_bank_account(recipient_id: str, bank_account_id: str) -> Dict[str, Any]:
        """Obtém detalhes de uma conta bancária específica."""
        url = f"{PagarMeBankAccountsAPI.BASE_URL}/recipients/{recipient_id}/bank_accounts/{bank_account_id}"
        headers = PagarMeBankAccountsAPI._get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me bank account retrieved: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to get Pagar.me bank account: {e.response.json()}")
            raise Exception(f"Failed to get Pagar.me bank account: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error getting Pagar.me bank account: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def update_bank_account(recipient_id: str, bank_account_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza uma conta bancária existente."""
        url = f"{PagarMeBankAccountsAPI.BASE_URL}/recipients/{recipient_id}/bank_accounts/{bank_account_id}"
        headers = PagarMeBankAccountsAPI._get_headers()
        try:
            response = requests.patch(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me bank account updated: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to update Pagar.me bank account: {e.response.json()}")
            raise Exception(f"Failed to update Pagar.me bank account: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error updating Pagar.me bank account: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")