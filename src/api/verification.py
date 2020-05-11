import json
import jsonschema

from flask import jsonify, Response, request, json
from schemas.verify_schema import *
from phishing.url_verifier import *
from helpers.phishing_levels import PhishLevel
from helpers.url_helper import url_to_domain

from werkzeug.exceptions import BadRequest

def verify_by_all(): 
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, verify_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    verdict = verify_all(request_data.get('url'))
    response_text = { 
        "result": f"{verdict}" 
    }
    return Response(json.dumps(response_text), 200, mimetype="application/json")
    
def verify_by_cert_hole(): 
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, verify_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    domain = url_to_domain(request_data.get('url'))
    if verify_cert_hole(domain):
        verdict = PhishLevel.MALICIOUS.get('status')
    else:
        verdict = PhishLevel.GOOD.get('status')
        
    response_text = { 
        "result": f"{verdict}" 
    }
    return Response(json.dumps(response_text), 200, mimetype="application/json") 

def verify_by_levenstein(): 
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, verify_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    domain = url_to_domain(request_data.get('url'))
    if verify_levenstein(domain):
        verdict = PhishLevel.MALICIOUS.get('status')
    else:
        verdict = PhishLevel.GOOD.get('status')

    response_text = {
        "status": verdict
    }
    return Response(json.dumps(response_text), 200, mimetype="application/json")
    
    

def verify_by_entropy(): 
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, verify_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    domain = url_to_domain(request_data.get('url'))
    if verify_entropy(domain):
        verdict = PhishLevel.MALICIOUS.get('status')
    else:
        verdict = PhishLevel.GOOD.get('status')

    response_text = {
        "status": verdict
    }
    return Response(json.dumps(response_text), 200, mimetype="application/json")

def verify_by_whois(): 
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, verify_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    domain = url_to_domain(request_data.get('url'))
    if verify_whois(domain):
        verdict = PhishLevel.MALICIOUS.get('status')
    else:
        verdict = PhishLevel.GOOD.get('status')

    response_text = {
        "status": verdict
    }
    return Response(json.dumps(response_text), 200, mimetype="application/json")
    
    

def verify_by_sfbrowsing(): 
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, verify_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    if verify_safebrowsing(request_data.get('url')):
        verdict = PhishLevel.MALICIOUS.get('status')
    else:
        verdict = PhishLevel.GOOD.get('status')

    response_text = {
        "status": verdict
    }
    return Response(json.dumps(response_text), 200, mimetype="application/json")

    

def verify_by_urlscan(): 
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, verify_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    verify, _ = verify_urlscan(request_data.get('url'), force_scan=True)
    if verify:
        verdict = PhishLevel.MALICIOUS.get('status')
    else:
        verdict = PhishLevel.GOOD.get('status')

    response_text = {
        "status": verdict
    }
    return Response(json.dumps(response_text), 200, mimetype="application/json")
    

def verify_by_crt(): 
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, verify_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    domain = url_to_domain(request_data.get('url'))
    if verify_certsh(domain):
        verdict = PhishLevel.MALICIOUS.get('status')
    else:
        verdict = PhishLevel.GOOD.get('status')

    response_text = {
        "status": verdict
    }
    return Response(json.dumps(response_text), 200, mimetype="application/json")
    
    

def verify_by_keywords(): 
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, verify_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    domain = url_to_domain(request_data.get('url'))
    verify = verify_keyword_match(domain)
    if verify:
        verdict = PhishLevel.MALICIOUS.get('status')
    else:
        verdict = PhishLevel.GOOD.get('status')

    response_text = {
        "status": verdict
    }
    return Response(json.dumps(response_text), 200, mimetype="application/json")
    