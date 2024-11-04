import os
import csv
from collections import defaultdict

from src.database.mongo_crud import find_one_doc

from src.utilities.datetime import extract_month

from src.constants import TOP_PAGES_COLLECTION

def generate_top_pages_for_period_csv(START_DATE, END_DATE, reports_dir):
    SITE_ID = os.environ.get('MATOMO_SITE_ID')
    
    query = {
        "website_id": SITE_ID,
        "timeframe.start_date": START_DATE,
        "timeframe.end_date": END_DATE,
    }
    document = find_one_doc(TOP_PAGES_COLLECTION, query)
    
    file_path = f"{reports_dir}/top_pages.csv"
    create_csv_from_json_objects(document, file_path)

def create_csv_from_json_objects(document, file_path):
    if not document:
        return
    
    pages_summary = document.get("pages_summary") or {}
    keys = pages_summary[0].keys()
    
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        for obj in pages_summary:
            writer.writerow(obj)