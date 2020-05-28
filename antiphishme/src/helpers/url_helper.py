def url_to_domain(URL):
     return URL.replace("http://", '').replace("https://", '').split('/')[0].split('?')[0]