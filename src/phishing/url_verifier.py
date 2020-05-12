import logging as log 

from models.baddies_model import Baddies
from models.certs_model import Certs
from models.goodies_model import Goodies

from api_modules.safebrowsing import lookup_url, SafeBrowsingException
from api_modules.levenstein import levenstein_check
from api_modules.entropy import get_entropy
from api_modules import urlscan
from api_modules.keywords import match_keyword
import api_modules.whois_module as whois
import api_modules.crtsh as crtsh
import api_modules.cert_hole as ch

from datetime import datetime, timedelta
from helpers.phishing_levels import PhishLevel
from helpers.consts import Const
from helpers.url_helper import url_to_domain
from helpers import db_helper as db_h

def verify_domain_in_baddies(domain):
    baddies = Baddies.get_all_baddies()
    for b in baddies:
        if b.get('domain_name') == domain:
            return True
        else:
            continue
    return False

def verify_urlscan(URL, passive=False, urlscan_wait_time=Const.URLSCAN_WAIT_SECONDS):
    historic_search, when_performed = urlscan.search_newest(URL)
    
    if passive:
        time_delta = 3 * Const.DAY
    else:
        time_delta = Const.WEEK_DAYS

    if when_performed and when_performed > datetime.utcnow() - timedelta(days=time_delta):
        results = urlscan.results(historic_search.get('_id'))
        if results and results.get('malicious'):
            return True, Const.URLSCAN_FINISHED_MESSAGE
        else:
            return False, Const.URLSCAN_FINISHED_MESSAGE
    elif not passive:
        log.debug('[URL_VERIFY] Force scanning URL')
        try:
            url_id = urlscan.submit(URL)
        except urlscan.UrlscanException:
            return False, Const.URLSCAN_NOT_FINISHED_ERROR
        results = urlscan.results(url_id, wait_time=urlscan_wait_time)
        if results:
            if results.get('malicious'):
                return True, Const.URLSCAN_FINISHED_MESSAGE
            else:
                return False, Const.URLSCAN_FINISHED_MESSAGE
        else:
            return False, Const.URLSCAN_NOT_FINISHED_ERROR
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
    If length of keyword is less than 2 * length of domain phrase
        and length of domain phrase is longer than 2 (to exclude eg 'wp' or 'pl')
        and levenstein's distance is less than 3 and more than 0
        then increase lev's amount for keyword
    If amount of matches for a phrase from domain is less than half of amount of phrases
        then it is malicious
    else
        it is not

    """
    good_keywords = [k['good_keyword'] for k in Goodies.get_all_goodies()]
    domain_phrases = domain.split('.')
    verdict, _, _ = levenstein_check(good_keywords, domain_phrases)
    return verdict

def verify_keyword_match(domain):
    verdict, _ = match_keyword(domain)
    return verdict

def verify_entropy(URL):
    if get_entropy(URL) >= Const.ENTROPY_PHISHING_MIN:
        return True
    else:
        return False

def verify_safebrowsing(URL):
    try:
        return lookup_url(URL).get('malicious')
    except SafeBrowsingException:
        return False

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

    if not malicious and not in_db and crt_results:
        Certs.add_cert(
            _caid=crt_results.get('caid'), 
            _subject_organizationName=crt_results.get('subject').get('org_name'), 
            _subject_countryName=crt_results.get('subject').get('country'),
            _issuer_commonName=crt_results.get('issuer').get('common_name'),
            _registered_at=crt_results.get('registered_at'),
            _multi_dns=crt_results.get('multi_dns_amount')
        )
    elif malicious and not in_db and crt_results:
        Certs.add_cert(
            _caid=crt_results.get('caid'), 
            _subject_organizationName=crt_results.get('subject').get('org_name'), 
            _subject_countryName=crt_results.get('subject').get('country'),
            _issuer_commonName=crt_results.get('issuer').get('common_name'),
            _registered_at=crt_results.get('registered_at'),
            _multi_dns=crt_results.get('multi_dns_amount'),
            _is_bad=True
        )
    return malicious

def verify_whois(domain):
    whois_results = whois.get_results(domain)
    if not whois_results:
        return False
    else:
        creation_date = whois_results.get('creation_date')
        if creation_date and creation_date > datetime.utcnow() - timedelta(days=Const.LIFE_LEN_PHISHING_CERT) :
            return True
        elif not whois_results['name'] and not whois_results['org']:
            return True
        else:
            return False

def verify_cert_hole(domain):
    if domain in ch.get_phishing_domains():
        return True
    else:
        return False

def verify_all(URL):
    log.debug(f"[URL_VERIFY] Validation for \"{URL}\"")
    domain = url_to_domain(URL)
    RAW_URL = URL
    URL = URL.replace("http://", '').replace("https://", '')
    if verify_domain_in_baddies(domain):
        return PhishLevel.MALICIOUS.get('status')
    elif verify_cert_hole(domain):
        db_h.DBHelper(db_h.create_baddie, (domain,)).run()
        return PhishLevel.MALICIOUS.get('status')
    else:
        sf_verdict = verify_safebrowsing(RAW_URL)
        crt_verdict = verify_certsh(domain)
        whois_verdict = verify_whois(domain)
        urlscan_verdict, urlscan_message = verify_urlscan(RAW_URL, passive=True)
        leven_verdict = verify_levenstein(domain)
        entropy_verdict = verify_entropy(URL)
        keyword_match_verdict = verify_keyword_match(domain)
        final_points = 0
        # Scale 0 - 100
        if whois_verdict:
            log.debug("[URL_VERIFY] WHOIS validation - checked")
            final_points += 10
        if sf_verdict:
            log.debug("[URL_VERIFY] SAFEBROWSE validation - checked")
            final_points += 25
        if crt_verdict:
            log.debug("[URL_VERIFY] CERTSH validation - checked")
            final_points += 20
        if leven_verdict:
            log.debug("[URL_VERIFY] LEVEN validation - checked")
            final_points += 15
        if entropy_verdict:
            log.debug("[URL_VERIFY] ENTROPY validation - checked")
            final_points += 5
        if keyword_match_verdict:
            log.debug("[URL_VERIFY] KEYWORD MATCH validation - checked")
            final_points += 5
        if urlscan_message == Const.URLSCAN_FINISHED_MESSAGE and urlscan_verdict:
            log.debug("[URL_VERIFY] URLSCAN validation - checked")
            final_points += 30

        if final_points > 0:
            log.debug(f"[URL_VERIFY] Final points for \"{URL}\": {final_points}")

        if final_points < PhishLevel.GOOD.get('max_level'):
            return PhishLevel.GOOD.get('status')
        elif final_points < PhishLevel.SUSPICIOUS.get('max_level'):
            return PhishLevel.SUSPICIOUS.get('status')
        else:
            db_h.DBHelper(db_h.create_baddie, (domain,)).run()
            return PhishLevel.MALICIOUS.get('status')
