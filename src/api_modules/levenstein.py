from Levenshtein import distance

def calculate_levenstein(base, target):
    return distance(base, target)

def levenstein_check(keywords, phrases_to_check):
    """

    Gets list of keywords eg ['facebook', 'google', 'onet']
    Gets list of phrases to check against keywords eg ['weka', 'pwr', 'edu', 'pl']
    Prepares dict for levenstein's values: {
        'keyword': 0
    }
    Do not compare if given keyword is same as phrase
    If length of keyword is less than 2 * legth of phrase
        and length of phrase is longer than 3 (to exclude eg 'wp' or 'pl')
        and levenstein's distance is less than 3 and more than 0
        then increase lev's amount for keyword
    If amount of matches for a phrase from domain is less than half of amount of phrases
        then it is malicious
    else
        it is not

    """
    levs = dict()
    for keyword in keywords:
        levs[keyword] = {
            'hits': 0,
            'match_keyword': ''
        }
    for keyword in keywords:
        for phrase in phrases_to_check:
            if keyword == phrase:
                continue
            elif len(keyword) < 2 * len(phrase) \
            and len(phrase) > 3 \
            and 0 < calculate_levenstein(keyword, phrase) < 3: 
                levs[keyword]['hits'] += 1
                levs[keyword]['match_keyword'] = keyword
            else:
                continue
    for key in levs:
        if levs[key]['hits'] != 0 and levs[key]['hits'] <= int(len(phrases_to_check) / 2):
            return True, levs[key]['hits'], levs[key]['match_keyword']
        else:
            continue
    return False, None, None
