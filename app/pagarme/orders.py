import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any, List
import logging
import base64

load_dotenv()

logger = logging.getLogger(__name__)

class PagarMeOrdersAPI:
    BASE_URL = "https://api.pagar.me/core/v5"
    API_KEY = os.getenv("PAGARME_API_KEY")

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        """Retorna headers comuns para chamadas à API."""
        return {
            "Authorization": f"Basic {base64.b64encode(f'{PagarMeOrdersAPI.API_KEY}:'.encode()).decode()}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def create_order(data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um pedido na Pagar.me."""
        url = f"{PagarMeOrdersAPI.BASE_URL}/orders"
        headers = PagarMeOrdersAPI._get_headers()
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me order created: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to create Pagar.me order: {e.response.json()}")
            raise Exception(f"Failed to create Pagar.me order: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error creating Pagar.me order: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def list_orders(params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Lista todos os pedidos."""
        url = f"{PagarMeOrdersAPI.BASE_URL}/orders"
        headers = PagarMeOrdersAPI._get_headers()
        try:
            response = requests.get(url, params=params or {}, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me orders listed: {response.json()}")
            return response.json().get("data", [])
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to list Pagar.me orders: {e.response.json()}")
            raise Exception(f"Failed to list Pagar.me orders: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error listing Pagar.me orders: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def get_order(order_id: str) -> Dict[str, Any]:
        """Obtém detalhes de um pedido específico."""
        url = f"{PagarMeOrdersAPI.BASE_URL}/orders/{order_id}"
        headers = PagarMeOrdersAPI._get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me order retrieved: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to get Pagar.me order: {e.response.json()}")
            raise Exception(f"Failed to get Pagar.me order: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error getting Pagar.me order: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def update_order(order_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um pedido existente."""
        url = f"{PagarMeOrdersAPI.BASE_URL}/orders/{order_id}"
        headers = PagarMeOrdersAPI._get_headers()
        try:
            response = requests.patch(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me order updated: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to update Pagar.me order: {e.response.json()}")
            raise Exception(f"Failed to update Pagar.me order: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error updating Pagar.me order: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def delete_all_order_items(order_id: str) -> None:
        """Deleta todos os itens de um pedido."""
        url = f"{PagarMeOrdersAPI.BASE_URL}/orders/{order_id}/items"
        headers = PagarMeOrdersAPI._get_headers()
        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me order items deleted: order_id={order_id}")
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to delete Pagar.me order items: {e.response.json()}")
            raise Exception(f"Failed to delete Pagar.me order items: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error deleting Pagar.me order items: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def close_order(order_id: str) -> Dict[str, Any]:
        """Fecha um pedido."""
        url = f"{PagarMeOrdersAPI.BASE_URL}/orders/{order_id}/closed"
        headers = PagarMeOrdersAPI._get_headers()
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me order closed: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to close Pagar.me order: {e.response.json()}")
            raise Exception(f"Failed to close Pagar.me order: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error closing Pagar.me order: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")