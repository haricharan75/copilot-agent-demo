import json
import urllib.request
import urllib.parse
import os

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
VAULT_DNS = os.environ.get("VAULT_DNS")
VAULT_USERNAME = os.environ.get("VAULT_USERNAME")
VAULT_PASSWORD = os.environ.get("VAULT_PASSWORD")
VAULT_API_VERSION = "v24.1"


def lambda_handler(event, context):

    print(f"Tool Lambda called: {json.dumps(event)}")

    try:
        action = event.get("actionGroup", "")
        function = event.get("function", "")
        parameters = event.get("parameters", [])

        print(f"Action  : {action}")
        print(f"Function: {function}")

        if function in ["check_duplicate", "searchVeevaRecords"]:

            object_type = get_param(parameters, "object_type")
            print(f"Searching object_type: {object_type}")

            session_id = authenticate_veeva()
            if not session_id:
                return agent_response(
                    action, function, {"error": "Veeva authentication failed"}
                )

            records = search_veeva_records(session_id, object_type)

            return agent_response(
                action,
                function,
                {
                    "records": records,
                    "total_count": len(records),
                    "object_type": object_type,
                    "status": "success",
                },
            )

        else:
            return agent_response(
                action, function, {"error": f"Unknown function: {function}"}
            )

    except Exception as e:
        print(f"Tool Lambda error: {str(e)}")
        return agent_response(
            event.get("actionGroup", ""), event.get("function", ""), {"error": str(e)}
        )


def authenticate_veeva():
    try:
        auth_url = f"https://{VAULT_DNS}/api/{VAULT_API_VERSION}/auth"
        auth_data = urllib.parse.urlencode(
            {"username": VAULT_USERNAME, "password": VAULT_PASSWORD}
        ).encode("utf-8")

        auth_req = urllib.request.Request(
            auth_url,
            data=auth_data,
            method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        with urllib.request.urlopen(auth_req, timeout=10) as resp:
            auth_body = json.loads(resp.read().decode("utf-8"))
            session_id = auth_body.get("sessionId")

        if session_id:
            print("Veeva auth successful")
        else:
            print(f"Veeva auth failed: {auth_body}")

        return session_id

    except Exception as e:
        print(f"Veeva auth error: {str(e)}")
        return None


def search_veeva_records(session_id, object_type):
    try:
        # ─────────────────────────────────────
        # VQL for each supported object type
        # ─────────────────────────────────────
        if object_type == "product__v":
            vql = "SELECT id, name__v FROM product__v WHERE status__v = 'active__v'"
        elif object_type == "drug_product__v":
            vql = (
                "SELECT id, name__v FROM drug_product__v WHERE status__v = 'active__v'"
            )
        elif object_type == "drug_substance__v":
            vql = "SELECT id, name__v FROM drug_substance__v WHERE status__v = 'active__v'"
        elif object_type == "excipient__v":
            vql = "SELECT id, name__v FROM excipient__v WHERE status__v = 'active__v'"
        else:
            vql = f"SELECT id, name__v FROM {object_type} WHERE status__v = 'active__v'"

        query_url = (
            f"https://{VAULT_DNS}"
            f"/api/{VAULT_API_VERSION}/query"
            f"?q={urllib.parse.quote(vql)}"
        )

        query_req = urllib.request.Request(
            query_url,
            method="GET",
            headers={"Authorization": session_id, "Accept": "application/json"},
        )

        with urllib.request.urlopen(query_req, timeout=15) as resp:
            query_body = json.loads(resp.read().decode("utf-8"))

        records = query_body.get("data", [])
        print(f"Fetched {len(records)} records for {object_type}")
        return records

    except Exception as e:
        print(f"Veeva search error: {str(e)}")
        return []


def agent_response(action_group, function, result):
    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": action_group,
            "function": function,
            "functionResponse": {
                "responseBody": {"TEXT": {"body": json.dumps(result)}}
            },
        },
    }


def get_param(parameters, name):
    for param in parameters:
        if param.get("name") == name:
            return param.get("value", "product__v")
    return "product__v"
