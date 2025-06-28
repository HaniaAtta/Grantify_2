# import requests
# from bs4 import BeautifulSoup
# from scrapers.utils import get_user_agent, is_grant_open

# def scrape_usaid(url="https://www.usaid.gov/"):
#     headers = {'User-Agent': get_user_agent()}
#     try:
#         res = requests.get(url, headers=headers, timeout=10)
#         res.raise_for_status()
#         text = BeautifulSoup(res.text, 'html.parser').get_text()
#         return {'url': url, 'status': 'open' if is_grant_open(text) else 'closed'}
#     except Exception as e:
#         return {'url': url, 'status': 'error', 'error': str(e)}


import requests
from bs4 import BeautifulSoup
from scrapers.utils import get_user_agent, is_grant_open

def scrape_usaid(url="https://www.usaid.gov/work-usaid/funding"):
    # Custom keywords for USAID
    custom_keywords = [
        'funding opportunity open', 'rfa open', 'usaid accepting applications',
        'addenda open', 'solicitation open', 'currently accepting proposals'
    ]

    # Override the default open_keywords
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
