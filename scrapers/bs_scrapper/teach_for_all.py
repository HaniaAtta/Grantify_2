import requests
from bs4 import BeautifulSoup
from scrapers.utils import get_user_agent, is_grant_open

def scrape_teach_for_all(url="https://teachforall.org/network-graduate-school-partnerships"):
    # Custom keywords tailored to educational/fellowship/grant contexts
    custom_keywords = [
        'funding opportunity', 'grant opportunity', 'apply now',
        'open for applications', 'accepting proposals', 'support program',
        'partnership opportunity', 'educational funding', 'now open',
        'application window open', 'fellowship applications',
        'collaborate with us', 'open call', 'submit a proposal'
    ]

    # Inject custom keywords into the global checker
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
