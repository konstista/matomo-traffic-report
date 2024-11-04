import os
import json

from uuid import uuid4
from datetime import datetime, timezone
from loguru import logger

from src.utilities.datetime import extract_date_ranges, extract_month
from src.matomo.pages_data_for_period import get_pages_data_for_period
from src.database.mongo_crud import insert_one_doc, find_one_doc

from src.constants import TOP_PAGES_COLLECTION

def load_top_pages_for_period(start_date, end_date):
    SITE_ID = os.environ.get('MATOMO_SITE_ID')
    
    # Check is record for the same period exists
    match_query = {
        "page_url": SITE_ID,
        "timeframe.start_date": start_date,
        "timeframe.end_date": end_date,
    }
    matching_record = find_one_doc(TOP_PAGES_COLLECTION, match_query)
    if matching_record:
        logger.info(f'Skipping processing for date range: {start_date} - {end_date}...')
        return
    
    # Retrieve data from Matomo API
    api_response = get_pages_data_for_period(start_date, end_date)

    if api_response:
        # Generate Database Record
        record = create_top_pages_record(start_date, end_date, api_response)
        # Save record to database
        insert_one_doc(TOP_PAGES_COLLECTION, record)

def create_top_pages_record(start_date, end_date, api_response):
    SITE_ID = os.environ.get('MATOMO_SITE_ID')
    pages_summary = []
    
    for page_data in api_response:
        label = page_data.get("label") # Page slug
        nb_visits = page_data.get("nb_visits") or 0 # All visits
        entry_nb_visits = page_data.get("entry_nb_visits") or 0 # Entry visits
        nb_hits = page_data.get("nb_hits") or 0 # All page views
        bounce_rate = page_data.get("bounce_rate") or "N/A" # Bounce rate
        avg_time_on_page = page_data.get("avg_time_on_page") or 0 # Average time on page
        
        goals = page_data.get("goals") or {}
        nb_conversions_entry_total = 0
        for goal_key in goals:
            goal_value = goals[goal_key]
            nb_conversions_entry = goal_value.get("nb_conversions_entry") or 0
            nb_conversions_entry_total += nb_conversions_entry
            
        pages_summary.append({
            "label": label,
            "nb_visits": nb_visits,
            "entry_nb_visits": entry_nb_visits,
            "nb_hits": nb_hits,
            "bounce_rate": bounce_rate,
            "avg_time_on_page": avg_time_on_page,
            "nb_conversions_entry_total": nb_conversions_entry_total
        })
            
    return  {
        "guid": str(uuid4()),
        "website_id": SITE_ID,
        "timeframe": {
            "period": "range",
            "start_date": start_date,
            "end_date": end_date
        },
        "pages_summary": pages_summary,
        "raw_api_response": api_response,
        "meta": {
            "created_at": datetime.now(timezone.utc),
            "updated_at": None,
            "deleted_at": None
        }
    }

# def export_to_csv(objects, file_path):
#     if not objects:
#         return
    
#     keys = objects[0].keys()
    
#     with open(filename, 'w', newline='') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=keys)
#         writer.writeheader()
#         for obj in objects:
#             writer.writerow(obj)