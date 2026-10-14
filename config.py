import os

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

API_KEY = os.environ["CPEE_API_KEY"]
if not API_KEY.strip():
    raise ValueError("CPEE_API_KEY must not be empty.")

CLIENT_SECRET_FILE = "client_secret.json"

TOKEN_DIR = "tokens"

DEFAULT_USER_ID = "default"

HOST = "::1"

PORT = 9001

BASE_URL = os.environ.get(
    "BASE_URL",
    "http://localhost:9001"
)

OAUTH_REDIRECT_URI = os.environ.get(
    "OAUTH_REDIRECT_URI",
    f"{BASE_URL}/oauth2callback"
)
