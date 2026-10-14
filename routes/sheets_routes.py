from bottle import route, response

from utils.auth_utils import require_api_key
from utils.request_utils import require_json_fields
from services.google_sheets_service import get_service, auth_required_response
from config import DEFAULT_USER_ID


@route("/createSpreadsheet", method="POST")
def create_spreadsheet():
    auth_err = require_api_key()
    if auth_err:
        return auth_err

    p, err = require_json_fields(("spreadsheet_title",))
    if err:
        return err

    user_id = p.get("user_id", DEFAULT_USER_ID)

    service = get_service(user_id)
    if not service:
        response.status = 401
        response.content_type = "application/json"
        return auth_required_response(user_id)

    sheet_properties = {
        "title": str(p.get("sheet_name", "Sheet1"))
    }

    grid_properties = {}

    if "rows" in p:
        grid_properties["rowCount"] = int(p["rows"])

    if "columns" in p:
        grid_properties["columnCount"] = int(p["columns"])

    if grid_properties:
        sheet_properties["gridProperties"] = grid_properties

    sheet = {
        "properties": sheet_properties
    }

    body = {
        "properties": {
            "title": str(p["spreadsheet_title"])
        },
        "sheets": [
            sheet
        ]
    }

    try:
        result = service.spreadsheets().create(body=body).execute()

        response.content_type = "application/json"
        created_sheet = result["sheets"][0]["properties"]
        return {
            "ok": True,
            "operation": "createSpreadsheet",
            "spreadsheetId": result["spreadsheetId"],
            "sheetId": created_sheet["sheetId"],
            "sheetTitle": created_sheet["title"]
        }

    except Exception as e:
        response.status = 500
        response.content_type = "application/json"
        return {
            "ok": False,
            "operation": "createSpreadsheet",
            "error": str(e)
        }


@route("/createSheet", method="POST")
def create_sheet():
    auth_err = require_api_key()
    if auth_err:
        return auth_err

    p, err = require_json_fields(("spreadsheetId", "sheet_title"))
    if err:
        return err

    user_id = p.get("user_id", DEFAULT_USER_ID)

    service = get_service(user_id)
    if not service:
        response.status = 401
        response.content_type = "application/json"
        return auth_required_response(user_id)

    body = {
        "requests": [
            {
                "addSheet": {
                    "properties": {
                        "title": str(p["sheet_title"]),
                        "gridProperties": {
                            "rowCount": int(p.get("rows", 1000)),
                            "columnCount": int(p.get("columns", 26))
                        }
                    }
                }
            }
        ]
    }

    try:
        result = service.spreadsheets().batchUpdate(
            spreadsheetId=str(p["spreadsheetId"]),
            body=body
        ).execute()

        sheet_props = result["replies"][0]["addSheet"]["properties"]

        response.content_type = "application/json"
        return {
            "ok": True,
            "operation": "createSheet",
            "sheetId": sheet_props["sheetId"],
            "title": sheet_props["title"]
        }

    except Exception as e:
        response.status = 500
        response.content_type = "application/json"
        return {
            "ok": False,
            "operation": "createSheet",
            "error": str(e)
        }


@route("/deleteSheet", method="POST")
def delete_sheet():
    auth_err = require_api_key()
    if auth_err:
        return auth_err

    p, err = require_json_fields(("spreadsheetId", "sheetId"))
    if err:
        return err

    user_id = p.get("user_id", DEFAULT_USER_ID)

    service = get_service(user_id)
    if not service:
        response.status = 401
        response.content_type = "application/json"
        return auth_required_response(user_id)

    body = {
        "requests": [
            {
                "deleteSheet": {
                    "sheetId": int(p["sheetId"])
                }
            }
        ]
    }

    try:
        service.spreadsheets().batchUpdate(
            spreadsheetId=str(p["spreadsheetId"]),
            body=body
        ).execute()

        response.content_type = "application/json"
        return {
            "ok": True,
            "operation": "deleteSheet",
            "deletedSheetId": int(p["sheetId"])
        }

    except Exception as e:
        response.status = 500
        response.content_type = "application/json"
        return {
            "ok": False,
            "operation": "deleteSheet",
            "error": str(e)
        }


@route("/renameResource", method="POST")
def rename_resource():
    auth_err = require_api_key()
    if auth_err:
        return auth_err

    p, err = require_json_fields(("spreadsheetId", "resourceType", "newTitle"))
    if err:
        return err

    user_id = p.get("user_id", DEFAULT_USER_ID)

    service = get_service(user_id)
    if not service:
        response.status = 401
        response.content_type = "application/json"
        return auth_required_response(user_id)

    resource_type = str(p["resourceType"]).lower()

    if resource_type == "spreadsheet":
        body = {
            "requests": [
                {
                    "updateSpreadsheetProperties": {
                        "properties": {
                            "title": str(p["newTitle"])
                        },
                        "fields": "title"
                    }
                }
            ]
        }

    elif resource_type == "sheet":
        if "sheetId" not in p:
            response.status = 400
            response.content_type = "application/json"
            return {
                "ok": False,
                "operation": "renameResource",
                "error": "missing sheetId"
            }

        body = {
            "requests": [
                {
                    "updateSheetProperties": {
                        "properties": {
                            "sheetId": int(p["sheetId"]),
                            "title": str(p["newTitle"])
                        },
                        "fields": "title"
                    }
                }
            ]
        }

    else:
        response.status = 400
        response.content_type = "application/json"
        return {
            "ok": False,
            "operation": "renameResource",
            "error": "resourceType must be 'spreadsheet' or 'sheet'"
        }

    try:
        service.spreadsheets().batchUpdate(
            spreadsheetId=str(p["spreadsheetId"]),
            body=body
        ).execute()

        response.content_type = "application/json"
        return {
            "ok": True,
            "operation": "renameResource",
            "resourceType": resource_type,
            "newTitle": str(p["newTitle"])
        }

    except Exception as e:
        response.status = 500
        response.content_type = "application/json"
        return {
            "ok": False,
            "operation": "renameResource",
            "error": str(e)
        }


@route("/updateCell", method="POST")
def update_cell():
    auth_err = require_api_key()
    if auth_err:
        return auth_err

    p, err = require_json_fields(("spreadsheetId", "range", "value"))
    if err:
        return err

    user_id = p.get("user_id", DEFAULT_USER_ID)

    service = get_service(user_id)
    if not service:
        response.status = 401
        response.content_type = "application/json"
        return auth_required_response(user_id)

    body = {
        "values": [
            [p["value"]]
        ]
    }

    try:
        result = service.spreadsheets().values().update(
            spreadsheetId=str(p["spreadsheetId"]),
            range=str(p["range"]),
            valueInputOption="RAW",
            body=body
        ).execute()

        response.content_type = "application/json"
        return {
            "ok": True,
            "operation": "updateCell",
            "updatedRange": result.get("updatedRange"),
            "updatedCells": result.get("updatedCells")
        }

    except Exception as e:
        response.status = 500
        response.content_type = "application/json"
        return {
            "ok": False,
            "operation": "updateCell",
            "error": str(e)
        }


@route("/updateManyCells", method="POST")
def update_many_cells():
    auth_err = require_api_key()
    if auth_err:
        return auth_err

    p, err = require_json_fields(("spreadsheetId", "range", "values"))
    if err:
        return err

    user_id = p.get("user_id", DEFAULT_USER_ID)

    service = get_service(user_id)
    if not service:
        response.status = 401
        response.content_type = "application/json"
        return auth_required_response(user_id)

    values = p["values"]

    if isinstance(values, str):
        import json
        values = json.loads(values)

    body = {
        "values": values
    }

    try:
        result = service.spreadsheets().values().update(
            spreadsheetId=str(p["spreadsheetId"]),
            range=str(p["range"]),
            valueInputOption="RAW",
            body=body
        ).execute()

        response.content_type = "application/json"
        return {
            "ok": True,
            "operation": "updateManyCells",
            "updatedRange": result.get("updatedRange"),
            "updatedCells": result.get("updatedCells")
        }

    except Exception as e:
        response.status = 500
        response.content_type = "application/json"
        return {
            "ok": False,
            "operation": "updateManyCells",
            "error": str(e)
        }


@route("/appendData", method="POST")
def append_data():
    auth_err = require_api_key()
    if auth_err:
        return auth_err

    p, err = require_json_fields(("spreadsheetId", "range", "values"))
    if err:
        return err

    user_id = p.get("user_id", DEFAULT_USER_ID)

    service = get_service(user_id)
    if not service:
        response.status = 401
        response.content_type = "application/json"
        return auth_required_response(user_id)

    values = p["values"]

    if isinstance(values, str):
        import json
        values = json.loads(values)

    body = {
        "values": values
    }

    try:
        result = service.spreadsheets().values().append(
            spreadsheetId=str(p["spreadsheetId"]),
            range=str(p["range"]),
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()

        response.content_type = "application/json"
        return {
            "ok": True,
            "operation": "appendData",
            "updatedRange": result.get("updates", {}).get("updatedRange"),
            "updatedRows": result.get("updates", {}).get("updatedRows"),
            "updatedCells": result.get("updates", {}).get("updatedCells")
        }

    except Exception as e:
        response.status = 500
        response.content_type = "application/json"
        return {
            "ok": False,
            "operation": "appendData",
            "error": str(e)
        }


@route("/readData", method="POST")
def read_data():
    auth_err = require_api_key()
    if auth_err:
        return auth_err

    p, err = require_json_fields(("spreadsheetId", "range"))
    if err:
        return err

    user_id = p.get("user_id", DEFAULT_USER_ID)

    service = get_service(user_id)
    if not service:
        response.status = 401
        response.content_type = "application/json"
        return auth_required_response(user_id)

    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=str(p["spreadsheetId"]),
            range=str(p["range"])
        ).execute()

        response.content_type = "application/json"
        return {
            "ok": True,
            "operation": "readData",
            "range": result.get("range"),
            "values": result.get("values", [])
        }

    except Exception as e:
        response.status = 500
        response.content_type = "application/json"
        return {
            "ok": False,
            "operation": "readData",
            "error": str(e)
        }


@route("/formatRange", method="POST")
def format_range():
    auth_err = require_api_key()
    if auth_err:
        return auth_err

    p, err = require_json_fields(("spreadsheetId", "sheetId", "startRowIndex", "endRowIndex", "startColumnIndex", "endColumnIndex"))
    if err:
        return err

    user_id = p.get("user_id", DEFAULT_USER_ID)

    service = get_service(user_id)
    if not service:
        response.status = 401
        response.content_type = "application/json"
        return auth_required_response(user_id)

    repeat_cell = {
        "range": {
            "sheetId": int(p["sheetId"]),
            "startRowIndex": int(p["startRowIndex"]),
            "endRowIndex": int(p["endRowIndex"]),
            "startColumnIndex": int(p["startColumnIndex"]),
            "endColumnIndex": int(p["endColumnIndex"])
        },
        "cell": {
            "userEnteredFormat": {}
        },
        "fields": ""
    }

    fields = []

    if "bold" in p:
        repeat_cell["cell"]["userEnteredFormat"].setdefault("textFormat", {})["bold"] = bool(p["bold"])
        fields.append("userEnteredFormat.textFormat.bold")

    if "fontSize" in p:
        repeat_cell["cell"]["userEnteredFormat"].setdefault("textFormat", {})["fontSize"] = int(p["fontSize"])
        fields.append("userEnteredFormat.textFormat.fontSize")

    if "backgroundColor" in p:
        color = p["backgroundColor"]

        if isinstance(color, str):
            import json
            color = json.loads(color)

        repeat_cell["cell"]["userEnteredFormat"]["backgroundColor"] = color
        fields.append("userEnteredFormat.backgroundColor")

    if not fields:
        response.status = 400
        response.content_type = "application/json"
        return {
            "ok": False,
            "operation": "formatRange",
            "error": "no formatting fields provided"
        }

    repeat_cell["fields"] = ",".join(fields)

    body = {
        "requests": [
            {
                "repeatCell": repeat_cell
            }
        ]
    }

    try:
        service.spreadsheets().batchUpdate(
            spreadsheetId=str(p["spreadsheetId"]),
            body=body
        ).execute()

        response.content_type = "application/json"
        return {
            "ok": True,
            "operation": "formatRange",
            "formattedRange": repeat_cell["range"],
            "fields": fields
        }

    except Exception as e:
        response.status = 500
        response.content_type = "application/json"
        return {
            "ok": False,
            "operation": "formatRange",
            "error": str(e)
        }


@route("/resizeDimension", method="POST")
def resize_dimension():
    auth_err = require_api_key()
    if auth_err:
        return auth_err

    p, err = require_json_fields(("spreadsheetId", "sheetId", "dimension", "startIndex", "endIndex", "pixelSize"))
    if err:
        return err

    user_id = p.get("user_id", DEFAULT_USER_ID)
    service = get_service(user_id)
    if not service:
        response.status = 401
        response.content_type = "application/json"
        return auth_required_response(user_id)

    body = {
        "requests": [
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": int(p["sheetId"]),
                        "dimension": str(p["dimension"]).upper(),  # "ROWS" or "COLUMNS"
                        "startIndex": int(p["startIndex"]),
                        "endIndex": int(p["endIndex"])
                    },
                    "properties": {
                        "pixelSize": int(p["pixelSize"])
                    },
                    "fields": "pixelSize"
                }
            }
        ]
    }

    try:
        service.spreadsheets().batchUpdate(
            spreadsheetId=str(p["spreadsheetId"]),
            body=body
        ).execute()

        response.content_type = "application/json"
        return {
            "ok": True,
            "operation": "resizeDimension",
            "sheetId": int(p["sheetId"]),
            "dimension": str(p["dimension"]).upper(),
            "startIndex": int(p["startIndex"]),
            "endIndex": int(p["endIndex"]),
            "pixelSize": int(p["pixelSize"])
        }

    except Exception as e:
        response.status = 500
        response.content_type = "application/json"
        return {
            "ok": False,
            "operation": "resizeDimension",
            "error": str(e)
        }