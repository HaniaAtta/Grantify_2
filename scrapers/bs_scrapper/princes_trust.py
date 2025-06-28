import requests
from bs4 import BeautifulSoup
from scrapers.utils import get_user_agent, is_grant_open

def scrape_princes_trust(url="https://www.princes-trust.org.uk/"):
    # Prince's Trust-specific keywords
    custom_keywords = [
        'apply for support', 'open for applications', 'available funding',
        'accepting applications', 'grants available', 'financial support',
        'entrepreneurship funding', 'youth grant', 'startup support',
        'now open', 'apply now', 'applications open'
    ]

    # Override global keywords temporarily
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
