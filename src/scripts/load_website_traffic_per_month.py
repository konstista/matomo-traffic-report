import os
from uuid import uuid4
from datetime import datetime, timezone
from loguru import logger

from src.utilities.datetime import extract_date_ranges, extract_month
from src.matomo.month_data import get_month_data
from src.database.mongo_crud import insert_one_doc, find_one_doc

from src.constants import MONTHLY_TRAFFIC_COLLECTION

def load_website_traffic_per_month(START_DATE, END_DATE):
    SITE_ID = os.environ.get('MATOMO_SITE_ID')
    
    date_ranges = extract_date_ranges(START_DATE, END_DATE)
    
    for date_range in date_ranges:
        # Check is record for the same period exists
        match_query = {
            "website_id": SITE_ID,
            "timeframe.start_date": date_range["start_date"],
            "timeframe.end_date": date_range["end_date"]
        }
        matching_record = find_one_doc(MONTHLY_TRAFFIC_COLLECTION, match_query)
        if matching_record:
            logger.info(f'Skipping processing for date range: {date_range["start_date"]} - {date_range["end_date"]}...')
            continue
        
        api_response = get_month_data(date_range)
        if api_response:
            # Generate Database Record
            record = create_monthly_record(SITE_ID, date_range, api_response)
            # Save record to database
            insert_one_doc(MONTHLY_TRAFFIC_COLLECTION, record)


def create_monthly_record(SITE_ID, date_range, api_response):
    return {
        "guid": str(uuid4()),
        "website_id": SITE_ID,
        "timeframe": {
            "year_month": extract_month(date_range["start_date"]),
            "start_date": date_range["start_date"],
            "end_date": date_range["end_date"],
            "is_full_month": date_range["is_full_month"]
        },
        "traffic_data": {
            "nb_visits": api_response.get("nb_visits") or 0, # Total number of visits
            "nb_actions": api_response.get("nb_actions") or 0, # Total number of actions performed
            "nb_visits_converted": api_response.get("nb_visits_converted") or 0, # Total number of visits that converted at least a single goal
            "bounce_count": api_response.get("bounce_count") or 0, # ???
            "sum_visit_length": api_response.get("sum_visit_length") or 0, # Total time spent
            "max_actions": api_response.get("max_actions") or 0, # Maximum number of actions performed
            "bounce_rate": api_response.get("bounce_rate") or "N/A",
            "nb_actions_per_visit": api_response.get("nb_actions_per_visit") or 0, # ???
            "avg_time_on_site": api_response.get("avg_time_on_site") or 0, # Average visit duration
        },
        "raw_api_response": api_response,
        "meta": {
            "created_at": datetime.now(timezone.utc),
            "updated_at": None,
            "deleted_at": None
        }
    }