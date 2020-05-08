from flask import Response

from models.user_model import *
from models.baddies_model import *
from models.certs_model import *
from models.location_model import *
from models.goodies_model import *

def check_domain(): 
    response_text = '{ "message": "Database created." }'
    response = Response(response_text, 200, mimetype='application/json')
    return response


def check_ip():
    response = Response("ok", 200, mimetype='application/json')
    return response

def create_db():
    db.drop_all()
    db.create_all()
    User.add_user_td()
    Location.add_location_td()
    Certs.add_cert_td()
    Baddies.add_baddie_td()
    Goodie.add_goodie_td()
    response_text = '{ "message": "Database created." }'
    response = Response(response_text, 200, mimetype='application/json')
    return response


def welcome():
    response_text = '{ "message": "Hello, welcome to sdetAutomation flask-api" }'
    response = Response(response_text, 200, mimetype='application/json')
    return response


def health():
    response_text = '{ "status": "OK" }'
    response = Response(response_text, 200, mimetype='application/json')
    return response
