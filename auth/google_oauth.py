import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError

from config import (
    SCOPES,
    CLIENT_SECRET_FILE,
    TOKEN_DIR,
    DEFAULT_USER_ID,
    OAUTH_REDIRECT_URI
)


def get_token_path(user_id=None):
    if not user_id:
        user_id = DEFAULT_USER_ID

    os.makedirs(TOKEN_DIR, exist_ok=True)
    return os.path.join(TOKEN_DIR, f"{user_id}.json")


def token_exists(user_id=None):
    return os.path.exists(get_token_path(user_id))


def load_credentials(user_id=None):
    token_path = get_token_path(user_id)

    if not os.path.exists(token_path):
        return None

    return Credentials.from_authorized_user_file(token_path, SCOPES)


def save_credentials(creds, user_id=None):
    token_path = get_token_path(user_id)

    with open(token_path, "w") as token_file:
        token_file.write(creds.to_json())


def get_credentials(user_id=None):
    creds = load_credentials(user_id)

    if not creds:
        return None

    if creds.valid:
        return creds

    if creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            save_credentials(creds, user_id)
            return creds
        except RefreshError:
            token_path = get_token_path(user_id)

            if os.path.exists(token_path):
                os.remove(token_path)

            return None

    return None


def create_oauth_flow():
    return Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri=OAUTH_REDIRECT_URI,
        autogenerate_code_verifier=False
    )


def create_authorization_url(user_id=None):
    if not user_id:
        user_id = DEFAULT_USER_ID

    flow = create_oauth_flow()

    auth_url, _ = flow.authorization_url(
        prompt="consent",
        access_type="offline",
        include_granted_scopes="true",
        state=user_id
    )

    return auth_url


def exchange_code_for_credentials(code, user_id=None):
    if not user_id:
        user_id = DEFAULT_USER_ID

    flow = create_oauth_flow()
    flow.fetch_token(code=code)

    creds = flow.credentials
    save_credentials(creds, user_id)

    return creds