import requests
from bs4 import BeautifulSoup
from scrapers.utils import get_user_agent, is_grant_open

def scrape_wipo(url="https://www.wipo.int/en/web/awards/global/how-to-apply"):
    # WIPO-specific keywords
    custom_keywords = [
        'call for proposals', 'funding opportunity', 'grant opportunity',
        'apply now', 'accepting applications', 'open for submissions',
        'innovation challenge', 'intellectual property support',
        'now open', 'applications open', 'open call', 'competition open',
        'rfa open', 'funding available', 'grants open'
    ]

    # Override default keywords for this run
    import scrapers.utils
    scrapers.utils.open_keywords = custom_keywords

    headers = {'User-Agent': get_user_agent()}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        text = BeautifulSoup(res.text, 'html.parser').get_text()
        return {'url': url, 'status': 'open' if is_grant_open(text) else 'closed'}
    except Exception as e:
        return {'url': url, 'status': 'error', 'error': str(e)}
