import os

from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()

load_dotenv(dotenv_path)

REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

ACCESS_TOKEN_EXPIRATION = os.getenv("ACCESS_TOKEN_EXPIRATION")
REFRESH_TOKEN_EXPIRATION = os.getenv("REFRESH_TOKEN_EXPIRATION")
ALGORITHM = os.getenv("ALGORITHM")
API_KEY = os.getenv("API_KEY")
