import requests
from bs4 import BeautifulSoup
from scrapers.utils import get_user_agent, is_grant_open

def scrape_thecommonwealth(url="https://thecommonwealth.org/procurement "):
    # Custom keywords typically used by The Commonwealth
    custom_keywords = [
        'apply now', 'applications open', 'accepting applications',
        'call for proposals', 'funding opportunity', 'scholarship open',
        'fellowship open', 'grants available', 'submission deadline',
        'now accepting', 'open call', 'youth program open',
        'grant opportunity', 'training opportunity', 'call for proposals',
        'request for proposals (rfp)',
        'request for applications (rfa)',
        'funding opportunity',
        'open call',
        'grant opportunity'
    ]

    # Override default open_keywords in utils
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
