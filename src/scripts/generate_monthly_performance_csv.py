import csv
from collections import defaultdict

from src.database.mongo_crud import find_docs

from src.utilities.datetime import extract_date_ranges, extract_month

from src.constants import SINGLE_PAGE_DATA_COLLECTION

def generate_monthly_performance_csv(START_DATE, END_DATE, urls, reports_dir):
    date_ranges = extract_date_ranges(START_DATE, END_DATE)
    year_months = sorted(set([extract_month(range["start_date"]) for range in date_ranges]))
    
    query = {
        "page_url": {"$in": urls},
        "timeframe.period": "month",
        "timeframe.year_month": {"$in": year_months}
    }
    documents = find_docs(SINGLE_PAGE_DATA_COLLECTION, query)

    metrics = {
        "nb_hits": "nb_hits",
        "nb_visits": "total_visits",
        "entry_nb_visits": "entry_visits",
    }
    for metric_key in metrics:
        file_name = f"{metrics[metric_key]}_{START_DATE}_{END_DATE}.csv"
        file_path = f"{reports_dir}/{file_name}"
        
        create_csv_from_json_objects(metric_key, documents, file_path, year_months)
        

def create_csv_from_json_objects(metric_key, json_objects, output_csv, all_year_months):
    data = defaultdict(dict)
    
    # Extract data from JSON objects
    for json_data in json_objects:
        page_url = json_data['page_url']
        year_month = json_data['timeframe']['year_month']
        metric_value = json_data['page_data'][metric_key]
        data[page_url][year_month] = metric_value

    # Write data to CSV
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        header = ['page_url'] + all_year_months
        writer.writerow(header)
        
        # Write data rows
        for page_url, url_data in data.items():
            row = [page_url] + [url_data.get(month, '') for month in all_year_months]
            writer.writerow(row)
