from dotenv import load_dotenv
from os import getenv

load_dotenv(dotenv_path=".env")

TOKEN = getenv("TOKEN")
HOST = getenv("HOST")

API_KEY = getenv("API_KEY")
API_SECRET = getenv("API_SECRET")

CRYPTORANK = getenv("API_CRYPTORANK")