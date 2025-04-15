import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any
import logging
import base64

load_dotenv()

logger = logging.getLogger(__name__)

class PagarMeOrderItemsAPI:
    BASE_URL = "https://api.pagar.me/core/v5"
    API_KEY = os.getenv("PAGARME_API_KEY")

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        """Retorna headers comuns para chamadas à API."""
        return {
            "Authorization": f"Basic {base64.b64encode(f'{PagarMeOrderItemsAPI.API_KEY}:'.encode()).decode()}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def create_order_item(order_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um item de pedido na Pagar.me."""
        url = f"{PagarMeOrderItemsAPI.BASE_URL}/orders/{order_id}/items"
        headers = PagarMeOrderItemsAPI._get_headers()
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me order item created: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to create Pagar.me order item: {e.response.json()}")
            raise Exception(f"Failed to create Pagar.me order item: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error creating Pagar.me order item: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def update_order_item(order_id: str, item_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um item de pedido."""
        url = f"{PagarMeOrderItemsAPI.BASE_URL}/orders/{order_id}/items/{item_id}"
        headers = PagarMeOrderItemsAPI._get_headers()
        try:
            response = requests.patch(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me order item updated: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to update Pagar.me order item: {e.response.json()}")
            raise Exception(f"Failed to update Pagar.me order item: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error updating Pagar.me order item: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def delete_order_item(order_id: str, item_id: str) -> None:
        """Exclui um item de pedido."""
        url = f"{PagarMeOrderItemsAPI.BASE_URL}/orders/{order_id}/items/{item_id}"
        headers = PagarMeOrderItemsAPI._get_headers()
        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me order item deleted: order_id={order_id}, item_id={item_id}")
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to delete Pagar.me order item: {e.response.json()}")
            raise Exception(f"Failed to delete Pagar.me order item: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error deleting Pagar.me order item: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")