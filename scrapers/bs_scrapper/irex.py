import requests
from bs4 import BeautifulSoup
from scrapers.utils import get_user_agent, is_grant_open

def scrape_irex(url="https://www.irex.org/program/community-engagement-exchange-program-application-information"):
    # Custom keywords likely used by IREX for grants and program calls
    custom_keywords = [
        'accepting applications', 'fellowship open', 'apply now','open'
        'grant opportunity', 'open call', 'currently accepting applications',
        'funding opportunity', 'request for proposals', 'rfp open',
        'now accepting proposals', 'submission deadline', 'call for proposals'
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
