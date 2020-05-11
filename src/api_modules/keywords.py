from models.goodies_model import Goodies

def match_keyword(domain):
    good_keywords = [k['good_keyword'] for k in Goodies.get_all_goodies()]
    domain_phrases = domain.split('.')
    for phrase in domain_phrases:
        for keyword in good_keywords:
            if keyword in phrase and keyword != phrase:
                return True, keyword
    return False, None