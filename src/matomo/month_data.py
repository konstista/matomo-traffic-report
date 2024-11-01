import os
import requests

from datetime import datetime
from loguru import logger

def get_month_data(range):
    SIDE_ID = os.environ.get('MATOMO_SITE_ID')
    MATOMO_URL = os.environ.get('MATOMO_URL')
    MATOMO_API_TOKEN = os.environ.get('MATOMO_API_TOKEN')
    API_URL = f"{MATOMO_URL}/index.php"
    
    # Format dates
    start_date = datetime.strptime(range["start_date"], '%Y-%m-%d').strftime('%Y-%m-%d')
    end_date = datetime.strptime(range["end_date"], '%Y-%m-%d').strftime('%Y-%m-%d')

    params = {
        'module': 'API', 
        'idSite': SIDE_ID,
        'format': 'JSON', 
        'period': 'range', 
        'date': f'{start_date},{end_date}', 
        'method': 'VisitsSummary.get',
        'token_auth': MATOMO_API_TOKEN,
        'flat': 1
    }

    logger.info(f'Requesting data for date range: {start_date} - {end_date}')

    # Make API request (without trailing slash)
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        parsed_response = response.json()
        if parsed_response:
            return parsed_response[0]


    logger.warning(f"Failed to get monthly data for date range: {start_date} - {end_date}")
    return {}
