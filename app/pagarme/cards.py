import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any, List
import logging
import base64

load_dotenv()

logger = logging.getLogger(__name__)

class PagarMeCardsAPI:
    BASE_URL = "https://api.pagar.me/core/v5"
    API_KEY = os.getenv("PAGARME_API_KEY")

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        """Retorna headers comuns para chamadas à API."""
        return {
            "Authorization": f"Basic {base64.b64encode(f'{PagarMeCardsAPI.API_KEY}:'.encode()).decode()}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def create_card(data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um cartão na Pagar.me."""
        url = f"{PagarMeCardsAPI.BASE_URL}/cards"
        headers = PagarMeCardsAPI._get_headers()
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me card created: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to create Pagar.me card: {e.response.json()}")
            raise Exception(f"Failed to create Pagar.me card: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error creating Pagar.me card: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def list_cards(params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Lista todos os cartões."""
        url = f"{PagarMeCardsAPI.BASE_URL}/cards"
        headers = PagarMeCardsAPI._get_headers()
        try:
            response = requests.get(url, params=params or {}, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me cards listed: {response.json()}")
            return response.json().get("data", [])
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to list Pagar.me cards: {e.response.json()}")
            raise Exception(f"Failed to list Pagar.me cards: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error listing Pagar.me cards: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def get_card(card_id: str) -> Dict[str, Any]:
        """Obtém detalhes de um cartão específico."""
        url = f"{PagarMeCardsAPI.BASE_URL}/cards/{card_id}"
        headers = PagarMeCardsAPI._get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me card retrieved: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to get Pagar.me card: {e.response.json()}")
            raise Exception(f"Failed to get Pagar.me card: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error getting Pagar.me card: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def delete_card(card_id: str) -> None:
        """Exclui um cartão."""
        url = f"{PagarMeCardsAPI.BASE_URL}/cards/{card_id}"
        headers = PagarMeCardsAPI._get_headers()
        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Pagar.me card deleted: card_id={card_id}")
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to delete Pagar.me card: {e.response.json()}")
            raise Exception(f"Failed to delete Pagar.me card: {e.response.json()}")
        except Exception as e:
            logger.error(f"Unexpected error deleting Pagar.me card: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")