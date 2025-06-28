import requests
from bs4 import BeautifulSoup
from scrapers.utils import get_user_agent, is_grant_open

def scrape_icimod(url="https://www.icimod.org/film-grants-on-water-springs-2024/"):
    # Custom keywords specific to ICIMOD-type grants
    custom_keywords = [
     'funding opportunity', 'call for applications', 'open call',
    'environmental grant', 'spring water grant', 'currently open',
    'accepting proposals', 'application deadline', 'climate funding'
    ]

    # Override global keywords with ICIMOD-specific ones
    import scrapers.utils
    scrapers.utils.open_keywords = custom_keywords

    headers = {'User-Agent': get_user_agent()}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        text = BeautifulSoup(res.text, 'html.parser').get_text()
        return {
            'url': url,
            'status': 'open' if is_grant_open(text) else 'closed'
        }
    except Exception as e:
        return {
            'url': url,
            'status': 'error',
            'error': str(e)
        }
