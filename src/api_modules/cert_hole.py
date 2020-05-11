import requests

class CertHoleException(Exception):
    def __init__(self, message="hole.cert.pl exception"):
        self.message = message

class CertHole:
    def __init__(self, url="https://hole.cert.pl/domains/domains.json"):
        self.url = url
    
    def get_data(self):
        _headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'
        }
        resp = requests.get(self.url, headers=_headers)
        if resp.status_code == 200:
            return resp.json()
        else:
            raise CertHoleException

def get_phishing_domains():
    ch = CertHole()
    data = ch.get_data()
    phishing = []
    for d in data:
        if not d['DeleteDate']:
            phishing.append(d['DomainAddress'])
    return phishing
