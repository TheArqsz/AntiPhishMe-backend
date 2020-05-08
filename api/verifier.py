import json

from helpers.phishverifier import *
from flask import Response

def verify(): 
    is_mal, data = verify_all("enlace.santandrer.com.mx.tuservin.com")
    response_text = { 
        "message": f"{data}" 
        }
    response = Response(json.dumps(response_text), 200, mimetype='application/json')
    return response