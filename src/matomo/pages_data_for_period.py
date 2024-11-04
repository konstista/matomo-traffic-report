import os
import requests

from datetime import datetime
from loguru import logger

def get_pages_data_for_period(start_date, end_date, filter_limit = 200):
    SITE_ID = os.environ.get('MATOMO_SITE_ID')
    MATOMO_URL = os.environ.get('MATOMO_URL')
    MATOMO_API_TOKEN = os.environ.get('MATOMO_API_TOKEN')
    API_URL = f"{MATOMO_URL}/index.php"
    
    # Format dates
    start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y-%m-%d')

    params = {
        'module': 'API', 
        'idSite': SITE_ID,
        'format': 'JSON', 
        'period': 'range', 
        'date': f'{start_date},{end_date}', 
        'method': 'Actions.getPageUrls',
        'token_auth': MATOMO_API_TOKEN,
        'filter_limit': f"{filter_limit}",
        'flat': 1,
        'showtitle': 1
    }

    logger.info(f'Requesting top pages data for {start_date} - {end_date}')

    # Make API request (without trailing slash)
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        parsed_response = response.json()
        return parsed_response

    logger.warning(f"Failed to get top pages data for {start_date} - {end_date}")
    return {}
