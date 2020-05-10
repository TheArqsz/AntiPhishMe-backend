import json
import jsonschema

from flask import jsonify, Response, request, json
from datetime import datetime, timedelta, date
from schemas.details_schema import *
from messages.error_messages import error_message_helper

from helpers import whois_helper, safebrowsing, crtsh, url_helper, urlscan
from helpers import ip as ip_helper
from helpers.consts import Const

import logging as log

def get_ip_details(): 
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, details_ip_schema)
    except jsonschema.exceptions.ValidationError as exc:
        return Response(error_message_helper(exc.message), 400, mimetype="application/json")

    details = ip.get_info(request_data.get('ip'))
    response_text = {
        "details": details
    }
    return Response(json.dumps(
            response_text,
            default=_default_json_model
            ), 200, mimetype="application/json")
    

def get_ip_details_by_domain(): 
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, details_domain_schema)
    except jsonschema.exceptions.ValidationError as exc:
        return Response(error_message_helper(exc.message), 400, mimetype="application/json")

    domain = url_helper.url_to_domain(request_data.get('domain'))
    ip = ip_helper.get_ip(domain)
    if ip:
        details = ip_helper.get_ip_details(ip)
    else:
        details = Const.UNKNOWN_RESULTS_MESSAGE
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
        jsonschema.validate(request_data, details_domain_schema)
    except jsonschema.exceptions.ValidationError as exc:
        return Response(error_message_helper(exc.message), 400, mimetype="application/json")

    results = whois_helper.get_results(request_data.get('domain'))
    if not results:
        results = Const.UNKNOWN_RESULTS_MESSAGE

    print(results)
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
        jsonschema.validate(request_data, details_domain_schema)
    except jsonschema.exceptions.ValidationError as exc:
        return Response(error_message_helper(exc.message), 400, mimetype="application/json")

    try:
        results = safebrowsing.lookup_url(request_data.get('domain'))
    except safebrowsing.ApiKeyException as exc:
        log.error(exc)
        return Response(error_message_helper(exc.message), 401, mimetype="application/json")

    if not results:
        results = Const.UNKNOWN_RESULTS_MESSAGE

    response_text = {
        "details": results
    }
    return Response(json.dumps(response_text), 200, mimetype="application/json")
    

def get_crtsh_details():
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, details_domain_schema)
    except jsonschema.exceptions.ValidationError as exc:
        return Response(error_message_helper(exc.message), 400, mimetype="application/json")

    results = crtsh.get_results(request_data.get('domain'))
    if not results:
        results = Const.UNKNOWN_RESULTS_MESSAGE

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
        return Response(error_message_helper(exc.message), 400, mimetype="application/json")

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
            return Response(error_message_helper(exc.message), 401, mimetype="application/json")
        except urlscan.UrlscanException as exc:
            return Response(error_message_helper(exc.message), 400, mimetype="application/json")


        results = urlscan.results(url_id, wait_time=60)
        if not results:
            results = Const.UNKNOWN_RESULTS_MESSAGE

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