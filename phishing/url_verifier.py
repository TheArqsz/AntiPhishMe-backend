import helpers.crtsh as crtsh
import helpers.whois_helper as whois

from models.baddies_model import *
from models.certs_model import *
from models.ip_model import *
from models.goodies_model import *
from helpers.safebrowsing import lookup_url
from helpers.levenstein import calculate_levenstein
from helpers.entropy import get_entropy
from helpers import urlscan
from datetime import datetime, timedelta
from phishing.phishing_levels import PhishLevel
from helpers.consts import Const

def verify_domain_in_baddies(domain):
    baddies = Baddies.get_all_baddies()
    for b in baddies:
        if b.get('domain_name') == domain:
            return True
        else:
            continue
    return False

def verify_urlscan(URL):
    historic_search, when_performed = urlscan.search_newest(URL)
    if when_performed and when_performed > datetime.utcnow() - timedelta(days=Const.WEEK_DAYS):
        results = urlscan.results(historic_search.get('_id'))
        if results and results.get('malicious'):
            return True, Const.URLSCAN_FINISHED_MESSAGE
        else:
            return False, Const.URLSCAN_FINISHED_MESSAGE
    else:
        try:
            url_id = urlscan.submit(URL)
        except urlscan.UrlscanException:
            return False, Const.URLSCAN_NOT_FINISHED_ERROR
        results = urlscan.results(url_id)
        if results:
            if results.get('malicious'):
                return True, Const.URLSCAN_FINISHED_MESSAGE
            else:
                return False, Const.URLSCAN_FINISHED_MESSAGE
        else:
            return False, Const.URLSCAN_NOT_FINISHED_ERROR

def verify_levenstein(domain):
    """

    Prepares list of good_keywords eg ['facebook', 'google', 'onet']
    Splits domain by '.' eg ['weka', 'pwr', 'edu', 'pl']
    Prepares dict for levenstein's values: {
        'keyword': 0
    }
    Do not compare if given keyword is same as domain
    If length of keyword is less than 2 * legth of domain phrase
        and length of domain phrase is longer than 2 (to exclude eg 'wp' or 'pl')
        and levenstein's distance is less than 3 and more than 0
        then increase lev's amount for keyword
    If amount of matches for a phrase from domain is less than half of amount of phrases
        then it is malicious
    else
        it is not

    """
    good_keywords = [k['good_keyword'] for k in Goodie.get_all_goodies()]
    domain_phrases = domain.split('.')
    levs = dict()
    for keyword in good_keywords:
        levs[keyword] = 0
    for keyword in good_keywords:
        for phrase in domain_phrases:
            if keyword == phrase:
                continue
            elif len(keyword) < 2 * len(phrase) \
            and len(phrase) > 2 \
            and 0 < calculate_levenstein(keyword, phrase) < 3: 
                levs[keyword] += 1
            else:
                continue
    #TOASK need help TODO Add something to check if keyword is in domain eg santander-costam.com
    for key in levs:
        if levs[key] != 0 and levs[key] <= int(len(domain_phrases) / 2):
            return True
        else:
            continue
    return False

def verify_entropy(URL):
    if get_entropy(URL) >= Const.ENTROPY_PHISHING_MIN:
        return True
    else:
        return False


def verify_safebrowsing(URL):
    return lookup_url(URL).get(URL).get('malicious')

def verify_certsh(domain):
    crt_results = crtsh.get_results(domain) 
    in_db = False
    malicious = False
    if not crt_results:
        malicious = True
    else:
        certs = Certs.get_all_certs()
        for c in certs:
            if crt_results.get('caid') == c.get('caid'):
                malicious = c.get('is_bad') 
                in_db = True

    if not in_db and crt_results:
        Certs.add_cert(
            _caid=crt_results.get('caid'), 
            _subject_organizationName=crt_results.get('subject').get('org_name'), 
            _subject_countryName=crt_results.get('subject').get('country'),
            _issuer_commonName=crt_results.get('issuer').get('common_name'),
            _registered_at=crt_results.get('registered_at'),
            _multi_dns=crt_results.get('multi_dns_amount')
        )
    return malicious

def verify_whois(domain):
    whois_results = whois.get_results(domain)
    if not whois_results:
        return False
    creation = whois_results.get('creation_date')
    if creation and creation > datetime.utcnow() - timedelta(days=Const.LIFE_LEN_PHISHING_CERT):
        return True
    else:
        return False



def verify_all(URL):
    domain = _url_to_domain(URL)
    URL = URL.replace("http://", '').replace("https://", '')
    if verify_domain_in_baddies(domain):
        # TOASK what does it mean - TODO return data from crt and ip db + malicious
        return PhishLevel.MALICIOUS.get('status')
    else:
        sf_verdict = verify_safebrowsing(URL)
        crt_verdict = verify_certsh(domain)
        whois_verdict = verify_whois(domain)
        urlscan_verdict, urlscan_message = verify_urlscan(URL)
        leven_verdict = verify_levenstein(domain)
        entropy_verdict = verify_entropy(URL)
        final_points = 0
        # 0 - 100
        if whois_verdict:
            print("WHOIS + 10")
            final_points += 10
        if sf_verdict:
            print("SAFEBROWSE + 30")
            final_points += 30
        if crt_verdict:
            print("CERTSH + 20")
            final_points += 20
        if leven_verdict:
            print("LEVEN + 15")
            final_points += 15
        if entropy_verdict:
            print("ENTROPY + 5")
            final_points += 5
        if urlscan_message == Const.URLSCAN_FINISHED_MESSAGE and urlscan_verdict:
            print("URLSCAN + 30")
            final_points += 30

        print('POINTS: ' + str(final_points))

        if final_points < PhishLevel.GOOD.get('max_level'):
            return PhishLevel.GOOD.get('status')
        elif final_points < PhishLevel.SUSPICIOUS.get('max_level'):
            return PhishLevel.SUSPICIOUS.get('status')
        else:
            _create_baddie(domain)
            return PhishLevel.MALICIOUS.get('status')

def _create_baddie(domain):
    # TODO add something to IP, certs and baddies
    pass

def _url_to_domain(URL):
     return URL.replace("http://", '').replace("https://", '').split('/')[0].split('?')[0]