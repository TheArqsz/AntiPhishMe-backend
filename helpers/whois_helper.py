import whois
import json
from datetime import datetime

def get_results(domain):
    d = dict()
    try:
        res = whois.whois(domain)
    except:
        return None
    d['registrar'] = res.get('registrar', None)
    if isinstance(res.get('creation_date'), list):
        d['creation_date'] = res.get('creation_date')[0]
    else:
        d['creation_date'] = res.get('creation_date')
    d['name'] = res.get('name', None)
    d['org'] = res.get('org', None)
    d['country'] = res.get('country', None)
    return d