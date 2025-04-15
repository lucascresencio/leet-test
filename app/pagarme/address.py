import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any, List
import logging
import base64

load_dotenv()

logger = logging.getLogger(__name__)

class PagarMeAddressAPI:
    BASE_URL = "https://api.pagar.me/core/v5"
    API_KEY = os.getenv("PAGARME_API_KEY")

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        """Retorna headers comuns para chamadas à API."""
        return {
            "Authorization": f"Basic {base64.b64encode(f'{PagarMeAddressAPI.API_KEY}:'.encode()).decode()}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def create_address(customer_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um endereço para um cliente na Pagar.me."""
        url = f"{PagarMeAddressAPI.BASE_URL}/customers/{customer_id}/addresses"
        headers = PagarMeAddressAPI._get_headers()
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me address created for customer {customer_id}: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to create Pagar.me address: {e.response.json()}")
            raise Exception(f"Failed to create Pagar.me address: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error creating Pagar.me address: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def list_addresses(customer_id: str) -> List[Dict[str, Any]]:
        """Lista todos os endereços de um cliente."""
        url = f"{PagarMeAddressAPI.BASE_URL}/customers/{customer_id}/addresses"
        headers = PagarMeAddressAPI._get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me addresses listed for customer {customer_id}: {response.json()}")
            return response.json().get("data", [])
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to list Pagar.me addresses: {e.response.json()}")
            raise Exception(f"Failed to list Pagar.me addresses: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error listing Pagar.me addresses: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def get_address(customer_id: str, address_id: str) -> Dict[str, Any]:
        """Obtém detalhes de um endereço específico."""
        url = f"{PagarMeAddressAPI.BASE_URL}/customers/{customer_id}/addresses/{address_id}"
        headers = PagarMeAddressAPI._get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me address retrieved: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to get Pagar.me address: {e.response.json()}")
            raise Exception(f"Failed to get Pagar.me address: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error getting Pagar.me address: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def update_address(customer_id: str, address_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um endereço existente."""
        url = f"{PagarMeAddressAPI.BASE_URL}/customers/{customer_id}/addresses/{address_id}"
        headers = PagarMeAddressAPI._get_headers()
        try:
            response = requests.patch(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me address updated: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to update Pagar.me address: {e.response.json()}")
            raise Exception(f"Failed to update Pagar.me address: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error updating Pagar.me address: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def delete_address(customer_id: str, address_id: str) -> None:
        """Exclui um endereço."""
        url = f"{PagarMeAddressAPI.BASE_URL}/customers/{customer_id}/addresses/{address_id}"
        headers = PagarMeAddressAPI._get_headers()
        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me address deleted: customer_id={customer_id}, address_id={address_id}")
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to delete Pagar.me address: {e.response.json()}")
            raise Exception(f"Failed to delete Pagar.me address: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error deleting Pagar.me address: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")