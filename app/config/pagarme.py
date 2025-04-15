import os
from dotenv import load_dotenv
import pagarme

load_dotenv()

def configure_pagarme():
    pagarme.authentication_key(os.getenv("PAGARME_API_KEY"))