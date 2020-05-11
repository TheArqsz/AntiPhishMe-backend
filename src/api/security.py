import json
import os

from flask import Response, request
from werkzeug.exceptions import Unauthorized

from config import AUTH_API_KEY

def verify_api(apikey, required_scopes):
    if apikey == AUTH_API_KEY:
        return {'sub': 'user'}
    else:
        raise Unauthorized
