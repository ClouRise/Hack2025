import os
from dotenv import load_dotenv


load_dotenv()
SECRET_KEY = "7a73351fa847dbc2318eb6774e4f81843c32268b6bae594fb12707f5f9de3bb8"

if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY not find")

ALGORITHM = "HS256"
