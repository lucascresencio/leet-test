from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client

#connect to database
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

#create maintainer user
def create_maintainer(name, ismaintainer: bool):
    response = supabase.table("profile").insert([
        { "name": name },
        { "ismaintainer": ismaintainer },
    ]).execute()

    return response



