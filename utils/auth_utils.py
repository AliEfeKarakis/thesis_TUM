from bottle import request, response

from config import API_KEY


def require_api_key():
    key = request.headers.get("X-API-Key")

    if not key:
        p = request.json
        if isinstance(p, dict):
            key = p.get("api_key")

    if not key:
        key = request.forms.get("api_key")

    if not key:
        key = request.query.get("api_key")

    if key != API_KEY:
        response.status = 401
        response.content_type = "application/json"
        return {
            "ok": False,
            "error_type": "unauthorized",
            "message": "Missing or invalid API key."
        }

    return None