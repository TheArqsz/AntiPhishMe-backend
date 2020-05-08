from time import sleep as wait
from socket import gethostbyname
from requests import get

def get_ip(domain):
    return gethostbyname(domain)

def get_ip_details(ip):
    url = f"http://ip-api.com/json/{ip}"
    tries = 5
    while tries != 0:
        response = get(url)
        if response.status_code == 429:
            wait(0.5)
            tries -= 1
        elif 'fail' in response.text:
            if 'reserved range' in response.text or 'private range' in response.text:
                return None
            return None
        else:
            wait(0.5)
            json = response.json()
            return {
                'country': json.get('countryCode'),
                'ip': ip,
                'asn': json.get('as')
            }

