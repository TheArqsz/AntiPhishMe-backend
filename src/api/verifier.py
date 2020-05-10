import json
import jsonschema

from flask import jsonify, Response, request, json
from schemas.verify_schema import *
from phishing.url_verifier import *
from messages.error_messages import *
from phishing.phishing_levels import PhishLevel

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

def verify_by_levenstein(): 
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, verify_domain_schema)
        if verify_levenstein(request_data.get('domain')):
            verdict = PhishLevel.MALICIOUS.get('status')
        else:
            verdict = PhishLevel.GOOD.get('status')

        response_text = {
            "status": verdict
        }
        response = Response(json.dumps(response_text), 200, mimetype="application/json")
    except jsonschema.exceptions.ValidationError as exc:
        response = Response(error_message_helper(exc.message), 400, mimetype="application/json")
    return response

def verify_by_entropy(): 
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, verify_domain_schema)
        if verify_entropy(request_data.get('domain')):
            verdict = PhishLevel.MALICIOUS.get('status')
        else:
            verdict = PhishLevel.GOOD.get('status')

        response_text = {
            "status": verdict
        }
        response = Response(json.dumps(response_text), 200, mimetype="application/json")
    except jsonschema.exceptions.ValidationError as exc:
        response = Response(error_message_helper(exc.message), 400, mimetype="application/json")
    return response

def verify_by_whois(): 
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, verify_domain_schema)
        if verify_whois(request_data.get('domain')):
            verdict = PhishLevel.MALICIOUS.get('status')
        else:
            verdict = PhishLevel.GOOD.get('status')

        response_text = {
            "status": verdict
        }
        response = Response(json.dumps(response_text), 200, mimetype="application/json")
    except jsonschema.exceptions.ValidationError as exc:
        response = Response(error_message_helper(exc.message), 400, mimetype="application/json")
    return response

def verify_by_sfbrowsing(): 
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, verify_url_schema)
        if verify_safebrowsing(request_data.get('url')):
            verdict = PhishLevel.MALICIOUS.get('status')
        else:
            verdict = PhishLevel.GOOD.get('status')

        response_text = {
            "status": verdict
        }
        response = Response(json.dumps(response_text), 200, mimetype="application/json")
    except jsonschema.exceptions.ValidationError as exc:
        response = Response(error_message_helper(exc.message), 400, mimetype="application/json")
    return response

def verify_by_urlscan(): 
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, verify_url_schema)
        verify, _ = verify_urlscan(request_data.get('url'))
        if verify:
            verdict = PhishLevel.MALICIOUS.get('status')
        else:
            verdict = PhishLevel.GOOD.get('status')

        response_text = {
            "status": verdict
        }
        response = Response(json.dumps(response_text), 200, mimetype="application/json")
    except jsonschema.exceptions.ValidationError as exc:
        response = Response(error_message_helper(exc.message), 400, mimetype="application/json")
    return response

def verify_by_crt(): 
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, verify_domain_schema)
        if verify_certsh(request_data.get('domain')):
            verdict = PhishLevel.MALICIOUS.get('status')
        else:
            verdict = PhishLevel.GOOD.get('status')

        response_text = {
            "status": verdict
        }
        response = Response(json.dumps(response_text), 200, mimetype="application/json")
    except jsonschema.exceptions.ValidationError as exc:
        response = Response(error_message_helper(exc.message), 400, mimetype="application/json")
    return response

def verify_by_keywords(): 
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, verify_domain_schema)
        verify, _ = verify_keyword_match(request_data.get('domain'))
        if verify:
            verdict = PhishLevel.MALICIOUS.get('status')
        else:
            verdict = PhishLevel.GOOD.get('status')

        response_text = {
            "status": verdict
        }
        response = Response(json.dumps(response_text), 200, mimetype="application/json")
    except jsonschema.exceptions.ValidationError as exc:
        response = Response(error_message_helper(exc.message), 400, mimetype="application/json")
    return response