import requests
from bs4 import BeautifulSoup
from scrapers.utils import get_user_agent, is_grant_open

def scrape_foodandwaterwatch(url="https://foodandwaterwatch.org"):
    # Custom keywords specific to Food & Water Watch announcements
    custom_keywords = [
        'grant opportunity', 'funding available', 'apply now',
        'accepting applications', 'call for proposals',
        'submissions open', 'application deadline', 'now accepting proposals',
        'grant round open', 'funding call open'
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
