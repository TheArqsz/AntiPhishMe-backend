import json
import jsonschema

from flask import jsonify, Response, request, json
from schemas.details_schema import *
from info import ip, domain
from messages.error_messages import *

import logging

def get_ip_details(): 
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, details_ip_schema)
        info = ip.get_info(request_data.get('ip'))
        response_text = info
        response = Response(json.dumps(response_text), 200, mimetype="application/json")
    except jsonschema.exceptions.ValidationError as exc:
        response = Response(error_message_helper(exc.message), 400, mimetype="application/json")
    return response

def get_domain_details(): 
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, details_domain_schema)
        info = domain.get_info(request_data.get('domain'))
        response_text = info
        response = Response(json.dumps(response_text), 200, mimetype="application/json")
    except jsonschema.exceptions.ValidationError as exc:
        response = Response(error_message_helper(exc.message), 400, mimetype="application/json")
    return response

def get_whois_details():
    return {}

def get_sfbrowsing_details():
    return {}

def get_crtsh_details():
    return {}

def get_urlscan_details():
    return {}