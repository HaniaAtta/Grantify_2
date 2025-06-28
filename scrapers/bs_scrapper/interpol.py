import requests
from bs4 import BeautifulSoup
from scrapers.utils import get_user_agent, is_grant_open

def scrape_interpol(url="https://www.interpol.int/"):
    # Custom keywords tailored to law enforcement, international collaboration, and funding
    custom_keywords = [
        'funding opportunity', 'grant opportunity', 'partnerships open',
        'call for proposals', 'submit application', 'now open',
        'accepting applications', 'open for collaboration',
        'project funding', 'open call', 'security grant',
        'law enforcement funding', 'apply now'
    ]

    # Override default keywords
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
