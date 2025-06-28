#!/usr/bin/env python3
import sys
import requests
from bs4 import BeautifulSoup
from scrapers.utils import get_user_agent, is_grant_open

# Force immediate output
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

def debug_print(msg):
    print(f"DEBUG: {msg}", file=sys.stderr, flush=True)

def scrape_poverty_action(url="https://poverty-action.org/open-funding-opportunities"):
    debug_print(f"Starting scrape of {url}")
    
    try:
        # Get headers
        headers = {'User-Agent': get_user_agent()}
        debug_print(f"Using headers: {headers}")
        
        # Make request
        debug_print("Making HTTP request...")
        response = requests.get(url, headers=headers, timeout=20)
        debug_print(f"Got status: {response.status_code}")
        response.raise_for_status()
        
        # Parse content
        debug_print("Parsing HTML...")
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(' ', strip=True)
        debug_print(f"Extracted {len(text)} characters")
        
        # Determine status
        status = 'open' if is_grant_open(text) else 'closed'
        debug_print(f"Status: {status}")
        
        return {
            'url': url,
            'status': status,
            'content_sample': text[:200] + '...'
        }
        
    except Exception as e:
        debug_print(f"ERROR: {str(e)}")
        return {
            'url': url,
            'status': 'error',
            'error': str(e)
        }

if __name__ == "__main__":
    debug_print("Script starting")
    try:
        result = scrape_poverty_action()
        print("FINAL RESULT:", result, flush=True)
    except Exception as e:
        debug_print(f"CRITICAL FAILURE: {str(e)}")
        sys.exit(1)