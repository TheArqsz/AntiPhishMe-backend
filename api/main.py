import json
import os

from flask import Response
from sqlalchemy import create_engine

from models.baddies_model import *
from models.certs_model import *
from models.goodies_model import *
from models.ip_model import *

from config import connexion_app

def create_db():
    db.drop_all()
    db.create_all()
    Certs.add_cert_td()
    IP.add_ip_td()
    Baddies.add_baddie_td()
    Goodie.add_goodie_td()
    response_text = {
        "message": "Database created."
    }
    response = Response(json.dumps(response_text), 200, mimetype='application/json')
    return response

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
    response = Response(json.dumps(response_text), 200, mimetype='application/json')
    return response

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