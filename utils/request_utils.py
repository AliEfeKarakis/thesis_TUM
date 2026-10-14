from bottle import request, response


def require_json_fields(fields):
    p = request.json

    if p is None:
        p = dict(request.forms)

    if not p:
        response.status = 400
        response.content_type = "application/json"
        return None, {"ok": False, "error": "invalid json or form data"}

    for field in fields:
        if field not in p:
            response.status = 400
            response.content_type = "application/json"
            return None, {"ok": False, "error": f"missing {field}"}

    return p, None