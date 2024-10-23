import json

from uuid import uuid4
from datetime import datetime, timezone
from loguru import logger

from src.utilities.datetime import extract_date_ranges, extract_month
from src.matomo.page_data import get_page_data
from src.database.mongo_crud import insert_one_doc, find_one_doc

from src.constants import SINGLE_PAGE_DATA_COLLECTION

def load_page_data_by_month(start_date, end_date, page_urls):
    date_ranges = extract_date_ranges(start_date, end_date)
    
    for page_url in page_urls:
        for range in date_ranges:
            # Check is record for the same period exists
            match_query = {
                "page_url": page_url,
                "timeframe.period": "month",
                "timeframe.start_date": range["start_date"],
                "timeframe.end_date": range["end_date"]
            }
            matching_record = find_one_doc(SINGLE_PAGE_DATA_COLLECTION, match_query)
            if matching_record:
                logger.info(f'Skipping processing for {page_url}, since existing record found in database.')
                continue
            
            # Retrieve data from Matomo API
            api_response = get_page_data(page_url, range)
            if api_response:
                # Generate Database Record
                record = create_monthly_record(page_url, range, api_response)
                # Save record to database
                insert_one_doc(SINGLE_PAGE_DATA_COLLECTION, record)

def create_monthly_record(page_url, range, api_response):
    return {
        "guid": str(uuid4()),
        "page_url": page_url,
        "timeframe": {
            "period": "month",
            "year_month": extract_month(range["start_date"]),
            "start_date": range["start_date"],
            "end_date": range["end_date"],
            "is_full_month": range["is_full_month"]
        },
        "page_data": {
            "nb_visits": api_response["nb_visits"], # All page visits
            "entry_nb_visits": api_response["entry_nb_visits"], # Page visits as entry page
            "exit_nb_visits": api_response["exit_nb_visits"], # Page visits that left website
            "avg_time_on_page": api_response["avg_time_on_page"], # Average time on page in seconds
            "bounce_rate": api_response["bounce_rate"], # Bounce rate in percent
            "exit_rate": api_response["exit_rate"], # Exit rate in percent
        },
        "raw_api_response": api_response,
        "meta": {
            "created_at": datetime.now(timezone.utc),
            "updated_at": None,
            "deleted_at": None
        }
    }