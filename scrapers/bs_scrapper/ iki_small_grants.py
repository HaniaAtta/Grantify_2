import requests
from bs4 import BeautifulSoup
from scrapers.utils import get_user_agent, is_grant_open

def scrape_iki_small_grants(url="https://iki-small-grants.de/application/"):
    # Custom keywords relevant to IKI Small Grants
    custom_keywords = [
          "Submit a project proposal", "open now","apply now"
     
    ]

    # Inject custom keywords into utils
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
