import os
import logging
from pysafebrowsing import SafeBrowsing

API_KEY = os.getenv("SAFEBROWSING_API_KEY") or None
s = SafeBrowsing(API_KEY)

def check_apikey():
    if API_KEY is None:
        logging.error("[SAFEBROWSING] No api key provided - set SAFEBROWSING_API_KEY env")
        raise ApiKeyException

class SafeBrowsingException(Exception):
    def __init__(self, message='safebrowsing exception'):
        self.message = message

class ApiKeyException(SafeBrowsingException):
    def __init__(self, message='safebrowsing authorization error'):
        self.message = message

def lookup_url(url):
    if not url:
        raise SafeBrowsingException
    check_apikey()
    results = s.lookup_urls([url])
    response = {
        'url': url,
        'malicious':  results.get(url).get('malicious')
    }
    return response