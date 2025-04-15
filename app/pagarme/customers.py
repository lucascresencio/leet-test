import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any, List
import logging
import base64

load_dotenv()

logger = logging.getLogger(__name__)

class PagarMeCustomerAPI:
    BASE_URL = "https://api.pagar.me/core/v5"
    API_KEY = os.getenv("PAGARME_API_KEY")

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        """Retorna headers comuns para chamadas à API."""
        return {
            "Authorization": f"Basic {base64.b64encode(f'{PagarMeCustomerAPI.API_KEY}:'.encode()).decode()}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def create_customer(data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um cliente na Pagar.me."""
        url = f"{PagarMeCustomerAPI.BASE_URL}/customers"
        headers = PagarMeCustomerAPI._get_headers()
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me customer created: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to create Pagar.me customer: {e.response.json()}")
            raise Exception(f"Failed to create Pagar.me customer: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error creating Pagar.me customer: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def list_customers(params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Lista todos os clientes."""
        url = f"{PagarMeCustomerAPI.BASE_URL}/customers"
        headers = PagarMeCustomerAPI._get_headers()
        try:
            response = requests.get(url, params=params or {}, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me customers listed: {response.json()}")
            return response.json().get("data", [])
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to list Pagar.me customers: {e.response.json()}")
            raise Exception(f"Failed to list Pagar.me customers: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error listing Pagar.me customers: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def get_customer(customer_id: str) -> Dict[str, Any]:
        """Obtém detalhes de um cliente específico."""
        url = f"{PagarMeCustomerAPI.BASE_URL}/customers/{customer_id}"
        headers = PagarMeCustomerAPI._get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me customer retrieved: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to get Pagar.me customer: {e.response.json()}")
            raise Exception(f"Failed to get Pagar.me customer: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error getting Pagar.me customer: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def update_customer(customer_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um cliente existente."""
        url = f"{PagarMeCustomerAPI.BASE_URL}/customers/{customer_id}"
        headers = PagarMeCustomerAPI._get_headers()
        try:
            response = requests.patch(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me customer updated: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to update Pagar.me customer: {e.response.json()}")
            raise Exception(f"Failed to update Pagar.me customer: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error updating Pagar.me customer: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def delete_customer(customer_id: str) -> None:
        """Exclui um cliente."""
        url = f"{PagarMeCustomerAPI.BASE_URL}/customers/{customer_id}"
        headers = PagarMeCustomerAPI._get_headers()
        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me customer deleted: customer_id={customer_id}")
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to delete Pagar.me customer: {e.response.json()}")
            raise Exception(f"Failed to delete Pagar.me customer: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error deleting Pagar.me customer: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")