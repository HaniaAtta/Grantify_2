import requests
from bs4 import BeautifulSoup
from scrapers.utils import get_user_agent, is_grant_open

def scrape_makingcents(url="https://makingcents.com"):
    # Custom keywords specific to Making Cents' typical offerings
    custom_keywords = [
        'apply now', 'accepting applications', 'request for proposals',
        'open rfp', 'funding opportunity', 'training opportunity',
        'consulting opportunity', 'now accepting', 'call for proposals',
        'submissions open', 'opportunity open', 'project funding'
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
