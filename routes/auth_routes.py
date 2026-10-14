from bottle import route, request, response

from auth.google_oauth import (
    create_authorization_url,
    get_credentials,
    exchange_code_for_credentials
)
from config import DEFAULT_USER_ID


@route("/authorize", method="GET")
def authorize():
    user_id = request.query.get("user_id") or DEFAULT_USER_ID

    response.content_type = "application/json"

    return {
        "ok": True,
        "user_id": user_id,
        "authorization_url": create_authorization_url(user_id)
    }


@route("/auth/status", method="GET")
def auth_status():
    user_id = request.query.get("user_id") or DEFAULT_USER_ID

    response.content_type = "application/json"

    creds = get_credentials(user_id)
    authorized = creds is not None

    result = {
        "ok": True,
        "user_id": user_id,
        "authorized": authorized
    }

    if not authorized:
        result["error_type"] = "auth_required"
        result["message"] = "Google authorization is required before this workflow can continue."
        result["authorization_url"] = create_authorization_url(user_id)
        result["next_step"] = "Open the authorization link, grant access, and start the workflow again."

    return result


@route("/oauth2callback", method="GET")
def oauth2callback():
    code = request.query.get("code")
    user_id = request.query.get("state") or DEFAULT_USER_ID
    error = request.query.get("error")

    response.content_type = "application/json"

    if error:
        response.status = 400
        return {
            "ok": False,
            "error_type": "oauth_error",
            "message": "Google authorization failed or was cancelled.",
            "details": error
        }

    if not code:
        response.status = 400
        return {
            "ok": False,
            "error_type": "missing_code",
            "message": "OAuth callback did not contain an authorization code."
        }

    try:
        exchange_code_for_credentials(code, user_id)

        return {
            "ok": True,
            "user_id": user_id,
            "authorized": True,
            "message": "Google authorization completed successfully. You can now start the workflow again."
        }

    except Exception as e:
        response.status = 500
        return {
            "ok": False,
            "error_type": "token_exchange_failed",
            "message": "OAuth code could not be exchanged for credentials.",
            "details": str(e)
        }