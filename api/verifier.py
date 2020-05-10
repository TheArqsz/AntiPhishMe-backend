import json
import jsonschema

from flask import jsonify, Response, request, json
from schemas.verify_schema import *
from phishing.url_verifier import *
from messages.error_messages import *

def verify_domain(): 
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, verify_domain_schema)
        verdict = verify_all(request_data.get('domain'))
        response_text = { 
            "result": f"{verdict}" 
        }
        response = Response(json.dumps(response_text), 200, mimetype="application/json")
    except jsonschema.exceptions.ValidationError as exc:
        response = Response(error_message_helper(exc.message), 400, mimetype="application/json")
    return response