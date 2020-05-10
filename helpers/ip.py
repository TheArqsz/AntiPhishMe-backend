import logging as log

from time import sleep as wait
from socket import gethostbyname
from requests import get

def get_ip(domain):
    try:
        return gethostbyname(domain)
    except:
        return None

def get_ip_details(ip):
    url = f"http://ip-api.com/json/{ip}"
    tries = 5
    while tries != 0:
        response = get(url)
        if response.status_code == 429:
            log.debug('[IP] Connection locked - trying again in 0.5 sec')
            wait(0.5)
            tries -= 1
        elif 'fail' in response.text:
            if 'reserved range' in response.text or 'private range' in response.text:
                return {
                    'ip': ip,
                    'status': 'reserved_range'
                }
            return None
        else:
            wait(0.5)
            json = response.json()
            return {
                'country': json.get('countryCode'),
                'ip': ip,
                'asn': json.get('as')
            }
    return None
