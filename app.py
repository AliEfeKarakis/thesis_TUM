from bottle import run

from config import HOST, PORT

import routes.health_routes
import routes.auth_routes
import routes.sheets_routes


if __name__ == "__main__":
    run(host=HOST, port=PORT, debug=True)
