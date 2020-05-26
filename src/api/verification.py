import json
import jsonschema

from flask import Response
from schemas.verify_schema import *
from phishing.url_verifier import *
from helpers.phishing_levels import PhishLevel
from helpers.url_helper import url_to_domain

from werkzeug.exceptions import BadRequest

def verify_by_all(url_body): 
    try:
        jsonschema.validate(url_body, verify_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    verdict = verify_all(url_body.get('url'))
    response_text = { 
        "result": f"{verdict}" 
    }
    return Response(json.dumps(response_text), 200, mimetype="application/json")
    
def verify_by_cert_hole(url_body): 
    try:
        jsonschema.validate(url_body, verify_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    domain = url_to_domain(url_body.get('url'))
    if verify_cert_hole(domain):
        verdict = PhishLevel.MALICIOUS.get('status')
    else:
        verdict = PhishLevel.GOOD.get('status')
        
    response_text = { 
        "result": f"{verdict}" 
    }
    return Response(json.dumps(response_text), 200, mimetype="application/json") 

def verify_by_levenstein(url_body): 
    try:
        jsonschema.validate(url_body, verify_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    domain = url_to_domain(url_body.get('url'))
    if verify_levenstein(domain):
        verdict = PhishLevel.MALICIOUS.get('status')
    else:
        verdict = PhishLevel.GOOD.get('status')

    response_text = {
        "status": verdict
    }
    return Response(json.dumps(response_text), 200, mimetype="application/json")
    
    

def verify_by_entropy(url_body): 
    try:
        jsonschema.validate(url_body, verify_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    if verify_entropy(url_body.get('url')):
        verdict = PhishLevel.MALICIOUS.get('status')
    else:
        verdict = PhishLevel.GOOD.get('status')

    response_text = {
        "status": verdict
    }
    return Response(json.dumps(response_text), 200, mimetype="application/json")

def verify_by_whois(url_body): 
    try:
        jsonschema.validate(url_body, verify_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    domain = url_to_domain(url_body.get('url'))
    if verify_whois(domain):
        verdict = PhishLevel.MALICIOUS.get('status')
    else:
        verdict = PhishLevel.GOOD.get('status')

    response_text = {
        "status": verdict
    }
    return Response(json.dumps(response_text), 200, mimetype="application/json")
    
    

def verify_by_sfbrowsing(url_body): 
    try:
        jsonschema.validate(url_body, verify_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    if verify_safebrowsing(url_body.get('url')):
        verdict = PhishLevel.MALICIOUS.get('status')
    else:
        verdict = PhishLevel.GOOD.get('status')

    response_text = {
        "status": verdict
    }
    return Response(json.dumps(response_text), 200, mimetype="application/json")

    

def verify_by_urlscan(url_body): 
    try:
        jsonschema.validate(url_body, verify_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    verify, _ = verify_urlscan(url_body.get('url'), passive=False, urlscan_wait_time=60)
    if verify:
        verdict = PhishLevel.MALICIOUS.get('status')
    else:
        verdict = PhishLevel.GOOD.get('status')

    response_text = {
        "status": verdict
    }
    return Response(json.dumps(response_text), 200, mimetype="application/json")
    

def verify_by_crt(url_body): 
    try:
        jsonschema.validate(url_body, verify_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    domain = url_to_domain(url_body.get('url'))
    if verify_certsh(domain):
        verdict = PhishLevel.MALICIOUS.get('status')
    else:
        verdict = PhishLevel.GOOD.get('status')

    response_text = {
        "status": verdict
    }
    return Response(json.dumps(response_text), 200, mimetype="application/json")
    
    

def verify_by_keywords(url_body): 
    try:
        jsonschema.validate(url_body, verify_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    domain = url_to_domain(url_body.get('url'))
    verify = verify_keyword_match(domain)
    if verify:
        verdict = PhishLevel.MALICIOUS.get('status')
    else:
        verdict = PhishLevel.GOOD.get('status')

    response_text = {
        "status": verdict
    }
    return Response(json.dumps(response_text), 200, mimetype="application/json")
    