from helpers import ip as ip_helper

def get_info(ip):
    info = ip_helper.get_ip_details(ip)
    if info:
        return info
    else:
        return 'Unknown'