import os
import threading
import time
import logging as log

from models.ip_model import IP
from models.baddies_model import Baddies 
from models.certs_model import Certs
from models.goodies_model import Goodies

from api_modules.ip_module import get_ip, get_ip_details
from api_modules import crtsh
from api_modules import levenstein as lev
from api_modules import entropy as ent
from api_modules.keywords import match_keyword

class DBHelper():
    """

    Class for running database methods in parallel to not interrupt usage of API.

    """
    def __init__(self, target=None, args=()):
        self.t = threading.Thread(target=target, args=args, daemon=True)

    def run(self):
        self.t.start()

def add_goodie(domain):
    pass

def add_cert(domain, is_bad=False):
    """

    Returns:
        True if successfully added cert + add id
        False if not successful and None

    """
    crt_results = crtsh.get_results(domain) 
    if not crt_results:
        return None
    
    crt_id = Certs.add_cert(
        crt_results.get('caid'),
        crt_results.get('subject').get('org_name'),
        crt_results.get('subject').get('country'),
        crt_results.get('issuer').get('common_name'),
        crt_results.get('registered_at'),
        crt_results.get('multi_dns_amount'),
        is_bad
    )
    if crt_id:
        return True, crt_id
    else:
        return None

def add_ip(domain):
    """

    Returns:
        True if successfully added ip + add id
        False if not successful and None

    """
    try:
        ip = get_ip(domain)
        success = True
    except Exception as e:
        log.error(e)
        success = False
    if success and ip:
        details = get_ip_details(ip) 
    else:
        return None
    ip_id = IP.add_ip(ip, details.get('country', None), details.get('asn', None))
    if ip_id:
        return True, ip_id
    else:
        return None
    
def add_baddie(domain, ip_id, crt_id, lev_d, lev_matched_keyword, contained_matched_keyword, entropy):
    return Baddies.add_baddie(domain, ip_id, crt_id, lev_d, lev_matched_keyword, contained_matched_keyword, entropy)

def create_baddie(domain):
    ip_id = add_ip(domain) or (False,-1)
    crt_id = add_cert(domain) or (False,-1)
    good_keywords = [k['good_keyword'] for k in Goodies.get_all_goodies()]
    domain_phrases = domain.split('.')
    _, _, lev_matched_keyword = lev.levenstein_check(good_keywords, domain_phrases) 
    
    min_lev_distance = 0
    lev_distance = 0
    if lev_matched_keyword:
        for phrase in domain_phrases:
            lev_distance = lev.calculate_levenstein(lev_matched_keyword, phrase)
            if 3 > min_lev_distance > lev_distance:
                min_lev_distance = lev_distance
    if not lev_matched_keyword:
        lev_matched_keyword = ''
    _, contained_matched_keyword = match_keyword(domain)
    if not contained_matched_keyword:
        contained_matched_keyword = ''
    entropy = ent.get_entropy(domain)
    return add_baddie(domain, ip_id[1], crt_id[1], lev_distance, lev_matched_keyword, contained_matched_keyword, entropy)

