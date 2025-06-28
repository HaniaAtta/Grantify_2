import requests
from bs4 import BeautifulSoup
from scrapers.utils import get_user_agent, is_grant_open

def scrape_goalglobal(url="https://www.goalglobal.org/innovationfund/"):
    # Custom keywords specific to GOAL Global Innovation Fund
    custom_keywords = [
        "applications open","call for proposals","apply now"

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
