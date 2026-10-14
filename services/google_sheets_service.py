from googleapiclient.discovery import build

from auth.google_oauth import get_credentials, create_authorization_url
from config import DEFAULT_USER_ID


def get_service(user_id=None):
    if not user_id:
        user_id = DEFAULT_USER_ID

    creds = get_credentials(user_id)

    if not creds:
        return None

    return build("sheets", "v4", credentials=creds)


def auth_required_response(user_id=None):
    if not user_id:
        user_id = DEFAULT_USER_ID

    return {
        "ok": False,
        "error_type": "auth_required",
        "message": "Google authorization is required before this workflow can be executed.",
        "authorization_url": create_authorization_url(user_id)
    }