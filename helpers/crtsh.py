import json

from pycrtsh import Crtsh

def get_results(domain):
    c = Crtsh()
    d = dict()
    certs = c.search(domain)
    if not certs:
        return None
    sorted_certs = sorted(certs, key=lambda k: k['logged_at'], reverse=True)
    newest = sorted_certs[0]
    d['caid'] = newest['ca'].get('caid', None)
    d['registered_at'] = newest.get('logged_at', None)
    cert = c.get(newest.get('id'))
    d['subject'] = dict()
    d['issuer'] = dict()
    d['subject']['org_name'] = cert['subject'].get('organizationName', None)
    d['subject']['country'] = cert['subject'].get('countryName', None)
    d['issuer']['common_name'] = cert['issuer'].get('commonName', None)
    d['multi_dns_amount'] = len(cert.get('extensions', []).get('alternative_names', []))
    return d