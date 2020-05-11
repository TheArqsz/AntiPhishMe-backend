import json

from pycrtsh import Crtsh
from helpers.url_helper import url_to_domain

def _search_domain(domain):
    """

    Check if domain exists in db of crt.sh and return it's certs

    """
    domain = url_to_domain(domain)
    c = Crtsh()
    certs = c.search(domain)
    if not certs:
        return None
    else:
        return certs

def _get_details(crt_id):
    """

    Returns details for given certificate

    """
    c = Crtsh()
    return c.get(crt_id)
        
def get_results(domain):
    certs = _search_domain(domain)
    if not certs:
        return None 
    d = dict()
    sorted_certs = sorted(certs, key=lambda k: k['logged_at'], reverse=True)
    newest = sorted_certs[0]
    d['caid'] = newest['ca'].get('caid', 'Unknown')
    d['registered_at'] = newest.get('logged_at', 'Unknown')
    cert = _get_details(newest.get('id'))
    d['subject'] = dict()
    d['issuer'] = dict()
    d['subject']['org_name'] = cert['subject'].get('organizationName', 'Unknown')
    d['subject']['country'] = cert['subject'].get('countryName', 'Unknown')
    d['issuer']['common_name'] = cert['issuer'].get('commonName', 'Unknown')
    d['multi_dns_amount'] = len(cert.get('extensions', [1]).get('alternative_names', [1]))
    return d