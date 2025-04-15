import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any, List
import logging
import base64

load_dotenv()

logger = logging.getLogger(__name__)

class PagarMePlanItemsAPI:
    BASE_URL = "https://api.pagar.me/core/v5"
    API_KEY = os.getenv("PAGARME_API_KEY")

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        """Retorna headers comuns para chamadas à API."""
        return {
            "Authorization": f"Basic {base64.b64encode(f'{PagarMePlanItemsAPI.API_KEY}:'.encode()).decode()}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def create_plan_item(plan_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um item de plano na Pagar.me."""
        url = f"{PagarMePlanItemsAPI.BASE_URL}/plans/{plan_id}/items"
        headers = PagarMePlanItemsAPI._get_headers()
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me plan item created: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to create Pagar.me plan item: {e.response.json()}")
            raise Exception(f"Failed to create Pagar.me plan item: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error creating Pagar.me plan item: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def list_plan_items(plan_id: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Lista itens de um plano."""
        url = f"{PagarMePlanItemsAPI.BASE_URL}/plans/{plan_id}/items"
        headers = PagarMePlanItemsAPI._get_headers()
        try:
            response = requests.get(url, params=params or {}, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me plan items listed: {response.json()}")
            return response.json().get("data", [])
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to list Pagar.me plan items: {e.response.json()}")
            raise Exception(f"Failed to list Pagar.me plan items: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error listing Pagar.me plan items: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def get_plan_item(plan_id: str, item_id: str) -> Dict[str, Any]:
        """Obtém detalhes de um item de plano específico."""
        url = f"{PagarMePlanItemsAPI.BASE_URL}/plans/{plan_id}/items/{item_id}"
        headers = PagarMePlanItemsAPI._get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me plan item retrieved: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to get Pagar.me plan item: {e.response.json()}")
            raise Exception(f"Failed to get Pagar.me plan item: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error getting Pagar.me plan item: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def update_plan_item(plan_id: str, item_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um item de plano."""
        url = f"{PagarMePlanItemsAPI.BASE_URL}/plans/{plan_id}/items/{item_id}"
        headers = PagarMePlanItemsAPI._get_headers()
        try:
            response = requests.patch(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me plan item updated: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to update Pagar.me plan item: {e.response.json()}")
            raise Exception(f"Failed to update Pagar.me plan item: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error updating Pagar.me plan item: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def delete_plan_item(plan_id: str, item_id: str) -> None:
        """Exclui um item de plano."""
        url = f"{PagarMePlanItemsAPI.BASE_URL}/plans/{plan_id}/items/{item_id}"
        headers = PagarMePlanItemsAPI._get_headers()
        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me plan item deleted: plan_id={plan_id}, item_id={item_id}")
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to delete Pagar.me plan item: {e.response.json()}")
            raise Exception(f"Failed to delete Pagar.me plan item: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error deleting Pagar.me plan item: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")