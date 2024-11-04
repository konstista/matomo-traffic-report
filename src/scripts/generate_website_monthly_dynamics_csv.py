import os
import csv
from collections import defaultdict

from src.database.mongo_crud import find_docs

from src.utilities.datetime import extract_date_ranges, extract_month

from src.constants import MONTHLY_TRAFFIC_COLLECTION

def generate_website_monthly_dynamics_csv(START_DATE, END_DATE, reports_dir):
    SIDE_ID = os.environ.get('MATOMO_SITE_ID')
    
    date_ranges = extract_date_ranges(START_DATE, END_DATE)
    year_months = sorted(set([extract_month(range["start_date"]) for range in date_ranges]))
    
    query = {
        "website_id": SIDE_ID,
        "timeframe.year_month": {"$in": year_months}
    }
    documents = find_docs(MONTHLY_TRAFFIC_COLLECTION, query)
    
    file_path = f"{reports_dir}/monthly_dynamics.csv"
    create_csv_from_json_objects(documents, year_months, file_path)

def create_csv_from_json_objects(documents, year_months, file_path):
# Extract unique year_month values and traffic_data fields
    traffic_fields = set()
    data = defaultdict(dict)

    for doc in documents:
        year_month = doc['timeframe']['year_month']
        
        for field, value in doc['traffic_data'].items():
            traffic_fields.add(field)
            data[year_month][field] = value

    # Sort year_months and traffic_fields
    year_months = sorted(year_months)
    traffic_fields = sorted(list(traffic_fields))

    # Write to CSV
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        header = ['year_month'] + traffic_fields
        writer.writerow(header)
        
        # Write data rows
        for year_month in year_months:
            row = [year_month] + [data[year_month].get(field, '') for field in traffic_fields]
            writer.writerow(row)
