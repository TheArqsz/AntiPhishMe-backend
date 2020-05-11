import json
import jsonschema
import logging as log

from flask import jsonify, Response, request, json
from datetime import datetime, timedelta, date
from schemas.details_schema import *

from api_modules import whois_module, safebrowsing, crtsh, urlscan, ip_module
from helpers.consts import Const
from helpers.url_helper import url_to_domain

from werkzeug.exceptions import BadRequest, Unauthorized

def get_ip_details(): 
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, details_ip_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    details = ip_module.get_ip_details(request_data.get('ip'))
    if not details:
        raise BadRequest('Wrong IP')

    response_text = {
        "details": details
    }
    return Response(json.dumps(
            response_text,
            default=_default_json_model
            ), 200, mimetype="application/json")
    

def get_ip_details_by_url(): 
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, details_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    domain = url_to_domain(request_data.get('url'))
    ip = ip_module.get_ip(domain)
    if ip:
        details = ip_module.get_ip_details(ip)
    else:
        raise BadRequest(Const.UNKNOWN_RESULTS_MESSAGE)

    response_text = {
        "details": details
    }
    return Response(json.dumps(
            response_text,
            default=_default_json_model
            ), 200, mimetype="application/json")


def get_whois_details():
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, details_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    domain = url_to_domain(request_data.get('url'))
    results = whois_module.get_results(domain)
    if not results:
        raise BadRequest(Const.UNKNOWN_RESULTS_MESSAGE)

    response_text = {
        "details": results
    }
    return Response(json.dumps(
            response_text,
            default=_default_json_model
            ), 200, mimetype="application/json")
    
    

def get_sfbrowsing_details():
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, details_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    try:
        results = safebrowsing.lookup_url(request_data.get('url'))
    except safebrowsing.ApiKeyException as exc:
        log.error(exc)
        raise Unauthorized(exc.message)

    if not results:
        raise BadRequest(Const.UNKNOWN_RESULTS_MESSAGE)

    response_text = {
        "details": results
    }
    return Response(json.dumps(response_text), 200, mimetype="application/json")
    

def get_crtsh_details():
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, details_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    domain = url_to_domain(request_data.get('url'))
    results = crtsh.get_results(domain)
    if not results:
        raise BadRequest(Const.UNKNOWN_RESULTS_MESSAGE)

    response_text = {
        "details": results
    }
    return Response(json.dumps(
            response_text,
            default=_default_json_model
            ), 200, mimetype="application/json")

def get_urlscan_details():
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, details_url_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise BadRequest(exc.message)

    URL = request_data.get('url')
    historic_search, when_performed = urlscan.search_newest(URL)
    found = False
    if when_performed and when_performed > datetime.utcnow() - timedelta(days=Const.WEEK_DAYS):
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
            raise BadRequest(Const.UNKNOWN_RESULTS_MESSAGE)

    response_text = {
        "details": results
    }
    return Response(json.dumps(
            response_text,
            default=_default_json_model
            ), 200, mimetype="application/json")

def _default_json_model(o):
    if isinstance(o, (date, datetime)):
        return o.isoformat()