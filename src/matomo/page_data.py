import os
import requests

from datetime import datetime
from loguru import logger

def get_page_data(page_url, range):
    SIDE_ID = os.environ.get('MATOMO_SITE_ID')
    MATOMO_URL = os.environ.get('MATOMO_URL')
    MATOMO_API_TOKEN = os.environ.get('MATOMO_API_TOKEN')
    API_URL = f"{MATOMO_URL}/index.php"
    
    # Format dates
    start_date = datetime.strptime(range["start_date"], '%Y-%m-%d').strftime('%Y-%m-%d')
    end_date = datetime.strptime( range["end_date"], '%Y-%m-%d').strftime('%Y-%m-%d')

    params = {
        'module': 'API', 
        'idSite': SIDE_ID,
        'format': 'JSON', 
        'period': 'range', 
        'date': f'{start_date},{end_date}', 
        'method': 'Actions.getPageUrl',
        'token_auth': MATOMO_API_TOKEN,
        'pageUrl': page_url
    }

    # Make API request
    logger.info(f'Requesting data for {page_url}; {start_date} - {end_date}')
    response = requests.get(API_URL, params=params)
    # Check if request was successful
    if response.status_code == 200:
        parsed_response = response.json()
        if not parsed_response:
            logger.info('Missing data for {page_url}; {start_date} - {end_date}. Fall back to empty value...')
            return {}
        else:
            return parsed_response[0]
    else:
        logger.warning(f"Error while getting page data.")
        logger.warning(f"Details: {response.status_code}, {response.text}")
        return 
