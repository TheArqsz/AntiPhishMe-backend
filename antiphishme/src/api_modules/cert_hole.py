from pycerthole import CertHole

def get_phishing_domains():
    ch = CertHole()
    return [d.domain_address for d in ch.get_data('txt')]