import json
import os

from flask import Response, request
from sqlalchemy import create_engine

from models.baddies_model import Baddies
from models.certs_model import Certs
from models.goodies_model import Goodies
from models.ip_model import IP
from db_config import db

from config import connexion_app

from werkzeug.exceptions import BadRequest

def create_db():
    db.drop_all()
    db.create_all()
    Certs.add_cert_td()
    IP.add_ip_td()
    Baddies.add_baddie_td()
    Goodies.add_goodie_td()
    response_text = {
        "message": "Database created."
    }
    return Response(json.dumps(response_text), 200, mimetype='application/json')

def health():
    # Check db
    if _db_status():
        db_status = 'OK'
    else:
        db_status = 'Error'
    
    response_text = {
        "db_status": db_status,
        "server_status": 'OK'
    }
    return Response(json.dumps(response_text), 200, mimetype='application/json')

def add_keyword():
    form = request.form
    if 'keyword' in form:
        keyword = form.get('keyword')
        if len(keyword) < 4:
            raise BadRequest('Keyword too short - min 4 signs')
        Goodies.add_goodie(keyword)
        response_text = {
            'status': 'OK'
        }
        return Response(json.dumps(response_text), 200, mimetype='application/json')
    else:
        raise BadRequest('No keyword in request')



def _db_status():
    db_uri = connexion_app.app.config['SQLALCHEMY_DATABASE_URI']
    if 'sqlite:///' in db_uri:
        t = db_uri.split('sqlite:///')[1]
        if not os.path.exists(t):
            return False
        else:
            return True
    else:
        try:
            engine = create_engine(db_uri, pool_recycle=3600)
            conn = engine.connect()
            conn.execute('SELECT 1;')
            return True
        except:
            return False
