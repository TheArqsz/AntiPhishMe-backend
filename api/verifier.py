import json

from helpers.phishverifier import *
from flask import Response

def verify(): 
    verdict = verify_all("prezydent.gov.pl")
    response_text = { 
        "result": f"{verdict}" 
        }
    response = Response(json.dumps(response_text), 200, mimetype='application/json')
    return response