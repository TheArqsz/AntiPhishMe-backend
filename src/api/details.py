import json
import jsonschema
import logging as log

from flask import Response
from datetime import datetime, timedelta, date
from schemas.details_schema import *

from api_modules import whois_module, safebrowsing, crtsh, urlscan, ip_module, levenstein, keywords, entropy
from helpers.consts import Const
from helpers.url_helper import url_to_domain

from models.goodies_model import Goodies

from werkzeug.exceptions import BadRequest, Unauthorized, HTTPException

def get_ip_details(ip_body): 
    try:
        jsonschema.validate(ip_body, details_ip_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)
    
    ip = ip_body.get('ip')
    if not ip or ip == "":
        raise BadRequest('Wrong IP')

    details = ip_module.get_ip_details(ip)
    if not details:
        raise BadRequest('Wrong IP')

    response_text = {
        "details": details
    }
    return Response(json.dumps(
            response_text,
            default=_default_json_model
            ), 200, mimetype="application/json")
    

def get_ip_details_by_url(url_body): 
    try:
        jsonschema.validate(url_body, details_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    domain = url_to_domain(url_body.get('url'))
    ip = ip_module.get_ip(domain)
    if ip:
        details = ip_module.get_ip_details(ip)
    else:
        return _no_data_response()

    response_text = {
        "details": details
    }
    return Response(json.dumps(
            response_text,
            default=_default_json_model
            ), 200, mimetype="application/json")


def get_whois_details(url_body):
    try:
        jsonschema.validate(url_body, details_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    domain = url_to_domain(url_body.get('url'))
    results = whois_module.get_results(domain)
    if not results:
        return _no_data_response()

    response_text = {
        "details": results
    }
    return Response(json.dumps(
            response_text,
            default=_default_json_model
            ), 200, mimetype="application/json")
    
    

def get_sfbrowsing_details(url_body):
    try:
        jsonschema.validate(url_body, details_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    try:
        results = safebrowsing.lookup_url(url_body.get('url'))
    except safebrowsing.ApiKeyException as exc:
        log.error(exc)
        raise Unauthorized(exc.message)

    if not results:
        return _no_data_response()

    response_text = {
        "details": results
    }
    return Response(json.dumps(response_text), 200, mimetype="application/json")
    

def get_crtsh_details(url_body):
    try:
        jsonschema.validate(url_body, details_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    domain = url_to_domain(url_body.get('url'))
    results = crtsh.get_results(domain)
    if not results:
        return _no_data_response()

    response_text = {
        "details": results
    }
    return Response(json.dumps(
            response_text,
            default=_default_json_model
            ), 200, mimetype="application/json")

def get_urlscan_details(url_body):
    try:
        jsonschema.validate(url_body, details_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    URL = url_body.get('url')
    historic_search, when_performed = urlscan.search_newest(URL)
    found = False
    if when_performed and when_performed > datetime.utcnow() - timedelta(days=Const.DAY):
        results = urlscan.results(historic_search.get('_id'))
        if results:
            found = True

    if not found:
        try:
            url_id = urlscan.submit(URL)
        except urlscan.ApiKeyException as exc:
            raise Unauthorized(exc.message)
        except urlscan.UrlscanException as exc:
            raise BadRequest(exc.message)

        results = urlscan.results(url_id, wait_time=60)
        if not results:
            return _no_data_response()

    response_text = {
        "details": results
    }
    return Response(json.dumps(
            response_text,
            default=_default_json_model
            ), 200, mimetype="application/json")

def get_levenstein_details(url_body):
    try:
        jsonschema.validate(url_body, details_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    domain = url_to_domain(url_body.get('url'))
    good_keywords = [k['good_keyword'] for k in Goodies.get_all_goodies()]
    domain_phrases = domain.split('.')
    _, _, lev_keyword, lev_dist = levenstein.levenstein_check(good_keywords, domain_phrases)
    if not lev_keyword:
        return _no_data_response()

    response_text = {
        "details": {
            "matched_keyword": lev_keyword,
            "levenstein_distance": lev_dist
        }
    }
    return Response(json.dumps(
            response_text,
            default=_default_json_model
            ), 200, mimetype="application/json")

def get_keyword_details(url_body):
    try:
        jsonschema.validate(url_body, details_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    domain = url_to_domain(url_body.get('url'))
    _, keyword = keywords.match_keyword(domain)
    if not keyword:
        return _no_data_response()

    response_text = {
        "details": {
            "matched_keyword": keyword
        }
    }
    return Response(json.dumps(
            response_text,
            default=_default_json_model
            ), 200, mimetype="application/json")
            
def get_entropy_details(url_body):
    try:
        jsonschema.validate(url_body, details_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message) 
    
    calculated = entropy.get_entropy(url_body.get('url'))

    response_text = {
        "details": {
            "entropy": round(calculated, 2)
        }
    }
    return Response(json.dumps(
            response_text,
            default=_default_json_model
            ), 200, mimetype="application/json")
            
def _default_json_model(o):
    if isinstance(o, (date, datetime)):
        return o.isoformat()

def _no_data_response(message=Const.EMPTY_RESPONSE_MESSAGE):
    resp = {
        'message': message
    }
    return Response(json.dumps(
            resp,
            default=_default_json_model
            ), 202, mimetype="application/json")