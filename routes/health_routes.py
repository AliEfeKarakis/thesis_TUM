from bottle import route, response


@route("/health", method="GET")
def health():
    response.content_type = "application/json"
    return {
        "ok": True
    }