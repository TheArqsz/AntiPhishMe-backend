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
    pass

class ApiKeyException(SafeBrowsingException):
    pass

def lookup_url(url):
    if not url:
        raise SafeBrowsingException
    check_apikey()
    return s.lookup_urls([url])

print(lookup_url('google'))