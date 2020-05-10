import whois
import json
from datetime import datetime
from helpers.url_helper import url_to_domain

def get_results(domain):
    domain = url_to_domain(domain)
    d = dict()
    try:
        res = whois.whois(domain)
    except:
        return None
    d['registrar'] = res.get('registrar', None)
    if isinstance(res.get('creation_date', None), list):
        d['creation_date'] = res.get('creation_date')[0]
    else:
        d['creation_date'] = res.get('creation_date', None)
    d['name'] = res.get('name', None)
    d['org'] = res.get('org', None)
    d['country'] = res.get('country', None)
    return d