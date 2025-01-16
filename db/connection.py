import os
from supabase import create_client
from dotenv import load_dotenv
load_dotenv()

#connect to database
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

def supabase_connection():
    supabase = create_client(url, key)
    return supabase
