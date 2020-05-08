import helpers.crtsh as crtsh
import helpers.whois_helper as whois

from models.baddies_model import *
from models.certs_model import *
from models.goodies_model import *
from helpers.safebrowsing import lookup_url
from helpers.levenstein import calculate_levenstein
from helpers.entropy import get_entropy
from datetime import datetime, timedelta

def verify_domain_in_baddies(domain):
    baddies = Baddies.get_all_baddies()
    for b in baddies:
        if b.get('domain_name') == domain:
            return True
        else:
            continue
    return False

def verify_levenstein(domain):
    good_keywords = [k['good_keyword'] for k in Goodie.get_all_goodies()]
    domain_phrases = domain.split('.')
    levs = dict()
    for keyword in good_keywords:
        levs[keyword] = 0
    for keyword in good_keywords:
        for phrase in domain_phrases:
            if keyword == phrase:
                continue
            elif len(keyword) < 2 * len(phrase) and len(phrase) > 2 and calculate_levenstein(keyword, phrase) < 3: 
                levs[keyword] += 1
            else:
                continue
    #TODO Add something to check if keyword is in domain
    for key in levs:
        if levs[key] != 0 and levs[key] <= int(len(domain_phrases) / 2):
            return True
        else:
            continue
    return False

def verify_entropy(URL):
    if get_entropy(URL) >= 3.65:
        return True
    else:
        return False


def verify_safebrowsing(URL):
    return lookup_url(URL).get(URL).get('malicious')

def verify_certsh(domain):
    crt_results = crtsh.get_results(domain) 
    if not crt_results:
        return False
    certs = Certs.get_all_certs()
    for c in certs:
        if crt_results.get('caid') == c.get('caid'):
            return c.get('is_bad') 
    # TODO
    # if crt_results:
    #     Certs.add_cert(
    #     _caid=crt_results.get('caid'), 
    #     _subject_organizationName=crt_results.get('subject').get('org_name'), 
    #     _subject_countryName=crt_results.get('subject').get('country'),
    #     _issuer_commonName=crt_results.get('issuer').get('common_name'),
    #     _registered_at=crt_results.get('registered_at'),
    #     _multi_dns=crt_results.get('multi_dns_amount')
    #     )
    return False

def verify_whois(domain):
    whois_results = whois.get_results(domain)
    if not whois_results:
        return False
    creation = whois_results.get('creation_date')
    if creation > datetime.utcnow() - timedelta(days=7):
        return True
    else:
        return False



def verify_all(URL):
    domain = URL.replace("http://", '').replace("https://", '').split('/')[0].split('?')[0]
    URL = URL.replace("http://", '').replace("https://", '')
    if verify_domain_in_baddies(domain):
        # TODO return data from crt and ip db + malicious
        return True, "No fałszywa no"
    else:
        sf_result = verify_safebrowsing(URL)
        crt_result = verify_certsh(domain)
        whois_result = verify_whois(domain)
        #TODO rethink urlscan
        leven_result = verify_levenstein(domain)
        entropy_result = verify_entropy(URL)
        final_result = 0
        # 0 - 100
        if whois_result:
            print("WHOIS + 10")
            final_result += 10
        if sf_result:
            print("SAFEBROWSE + 30")
            final_result += 30
        if crt_result:
            print("CERTSH + 20")
            final_result += 20
        if leven_result:
            print("LEVEN + 15")
            final_result += 15
        if entropy_result:
            print("ENTROPY + 5")
            final_result += 5
        # TODO
        # if urlscan_result:
        #     final_result += 30

        print('POINTS: ' + str(final_result))
        #TODO Add to baddies if malicious
        return sf_result, str(final_result)

