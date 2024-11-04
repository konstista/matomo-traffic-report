import os
import requests

from datetime import datetime
from loguru import logger

def get_pages_data_for_period(page_url, range, filter_limit = 100):
    SITE_ID = os.environ.get('MATOMO_SITE_ID')
    MATOMO_URL = os.environ.get('MATOMO_URL')
    MATOMO_API_TOKEN = os.environ.get('MATOMO_API_TOKEN')
    API_URL = f"{MATOMO_URL}/index.php"
    
    # Format dates
    start_date = datetime.strptime(range["start_date"], '%Y-%m-%d').strftime('%Y-%m-%d')
    end_date = datetime.strptime(range["end_date"], '%Y-%m-%d').strftime('%Y-%m-%d')

    params = {
        'module': 'API', 
        'idSite': SITE_ID,
        'format': 'JSON', 
        'period': 'range', 
        'date': f'{start_date},{end_date}', 
        'method': 'Actions.getPageUrls',
        'token_auth': MATOMO_API_TOKEN,
        'filter_limit': f"{filter_limit}",
        'flat': 1
    }

    logger.info(f'Requesting pages data for {page_url}; {start_date} - {end_date}')

    # Make API request (without trailing slash)
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        parsed_response = response.json()
        if parsed_response:
            return parsed_response[0]

    logger.warning(f"Failed to get page data for URL: {page_url}")
    return {}
