import requests
from bs4 import BeautifulSoup
from scrapers.utils import get_user_agent, is_grant_open

def scrape_unodc(url="https://www.unodc.org/unodc/en/human-trafficking-fund/unvtf-funding.html"):
    # Custom keywords specific to UNODC
    custom_keywords = [
       "applications are open","apply now","now open","submission deadline"

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
