import requests, json
import os
import logging
import time

API_KEY = os.getenv("URLSCAN_API_KEY") or None

def check_apikey():
    if API_KEY is None:
        logging.error("[URLSCAN] No api key provided - set URLSCAN_API_KEY env")
        raise ApiKeyException

class UrlscanException(Exception):
    pass

class ApiKeyException(UrlscanException):
    pass

def submit(url):
    global API_KEY
    print(API_KEY)
    headers = {
        'Content-Type': 'application/json',
        'API-Key': API_KEY,
    }
    data = {
        "url": f"{url}", 
        "public": "on"
    }
    response = requests.post('https://urlscan.io/api/v1/scan/', headers=headers, data=json.dumps(data))
    
    r = response.json()
    print(response.text)
    if r.get('message') and r.get('message') == "Submission successful":
        return r.get('uuid')
    else:
        logging.error("[URLSCAN] Cannot submit query")
        raise UrlscanException

def search(url):
    if '://' in url:
        url = url.split("://")[1]
    params = (
        ('q', f"domain:{url}"),
    )
    response = requests.get('https://urlscan.io/api/v1/search/', params=params)
    r = response.json()
    time.sleep(2)
    if r.get("total") > 0:
        return r.get("results")
    else:
        return None

def results(uuid):
    found = False
    duration = 0
    wait_time = 30
    while not found and duration < wait_time:
        response = requests.get(f"https://urlscan.io/api/v1/result/{uuid}")
        null_response_string = '"status": 404'
        r = response.content.decode("utf-8")
        if null_response_string in r:
            logging.warning(f"Results for {uuid} not processed. Please check again later.")
            time.sleep(2)
            duration += 2
        else:
            found = True
            logging.info(f"Results for {uuid} processed after {duration} sec.")
            j = response.json()
            return summary(response.json())
    return None

def summary(content):
    if content.get("data").get("requests")[0].get("response").get("failed"):
        return None
    ### relevant aggregate data
    request_info = content.get("data").get("requests")
    meta_info = content.get("meta")
    verdict_info = content.get("verdicts")
    list_info = content.get("lists")
    stats_info = content.get("stats")
    page_info = content.get("page")
    
    ### more specific data
    geoip_info = meta_info.get("processors").get("geoip") 
    web_apps_info = meta_info.get("processors").get("wappa")
    resource_info = stats_info.get("resourceStats")
    protocol_info = stats_info.get("protocolStats")
    ip_info = stats_info.get("ipStats")

    ### enumerate countries 
    countries = []
    for item in resource_info:
        country_list = item.get("countries")
        for country in country_list:
            if country not in countries:
                countries.append(country)

    ### enumerate web apps
    web_apps = []
    for app in web_apps_info.get("data"):
        web_apps.append(app.get("app"))
    
    ### enumerate domains pointing to ip
    pointed_domains = []
    for ip in ip_info:
        domain_list = ip.get("domains")
        for domain in domain_list:
            if domain not in pointed_domains:
                pointed_domains.append(domain)


    ### data for summary
    page_domain = page_info.get("domain")
    page_ip = page_info.get("ip")
    page_country = page_info.get("country")
    page_server = page_info.get("server")
    ads_blocked = stats_info.get("adBlocked")
    https_percentage = stats_info.get("securePercentage")
    ipv6_percentage = stats_info.get("IPv6Percentage")
    country_count = stats_info.get("uniqCountries")
    num_requests = len(request_info)
    is_malicious = verdict_info.get("overall").get("malicious")
    malicious_total = verdict_info.get("engines").get("maliciousTotal")
    ip_addresses = list_info.get("ips")
    urls = list_info.get("urls")

    results = {}
    results['domain'] = page_domain
    results['ip'] = page_ip
    results['country'] = page_country
    results['server'] = page_server
    results['webApps'] = web_apps
    results['no_of_requests'] = num_requests
    results['ads_blocked'] = ads_blocked
    results['https_requests'] = str(https_percentage) + "%"
    results['ipv6'] = str(ipv6_percentage) + "%"
    results['unique_country_count'] = country_count
    results['malicious'] = is_malicious
    results['malicious_requests'] = malicious_total
    results['pointed_domains'] = malicious_total

    return results