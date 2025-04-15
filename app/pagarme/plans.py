import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any, List
import logging
import base64

load_dotenv()

logger = logging.getLogger(__name__)

class PagarMePlansAPI:
    BASE_URL = "https://api.pagar.me/core/v5"
    API_KEY = os.getenv("PAGARME_API_KEY")

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        """Retorna headers comuns para chamadas à API."""
        return {
            "Authorization": f"Basic {base64.b64encode(f'{PagarMePlansAPI.API_KEY}:'.encode()).decode()}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def create_plan(data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um plano na Pagar.me."""
        url = f"{PagarMePlansAPI.BASE_URL}/plans"
        headers = PagarMePlansAPI._get_headers()
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me plan created: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to create Pagar.me plan: {e.response.json()}")
            raise Exception(f"Failed to create Pagar.me plan: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error creating Pagar.me plan: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def list_plans(params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Lista todos os planos."""
        url = f"{PagarMePlansAPI.BASE_URL}/plans"
        headers = PagarMePlansAPI._get_headers()
        try:
            response = requests.get(url, params=params or {}, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me plans listed: {response.json()}")
            return response.json().get("data", [])
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to list Pagar.me plans: {e.response.json()}")
            raise Exception(f"Failed to list Pagar.me plans: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error listing Pagar.me plans: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def get_plan(plan_id: str) -> Dict[str, Any]:
        """Obtém detalhes de um plano específico."""
        url = f"{PagarMePlansAPI.BASE_URL}/plans/{plan_id}"
        headers = PagarMePlansAPI._get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me plan retrieved: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to get Pagar.me plan: {e.response.json()}")
            raise Exception(f"Failed to get Pagar.me plan: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error getting Pagar.me plan: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def update_plan(plan_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um plano existente."""
        url = f"{PagarMePlansAPI.BASE_URL}/plans/{plan_id}"
        headers = PagarMePlansAPI._get_headers()
        try:
            response = requests.patch(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me plan updated: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to update Pagar.me plan: {e.response.json()}")
            raise Exception(f"Failed to update Pagar.me plan: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error updating Pagar.me plan: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")