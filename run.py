from dotenv import load_dotenv

from src.utilities.urls import load_urls_from_file
from src.scripts.load_page_data_by_month import load_page_data_by_month
from src.scripts.generate_monthly_performance_csv import generate_monthly_performance_csv

if __name__ == '__main__':
    load_dotenv()
    
    START_DATE = "2023-10-01"
    END_DATE = "2024-10-23"
    PAGES_FILE_PATH = "./data/pages.txt"
    
    # Reports
    MONTHLY_REPORTS_DIR = "./reports/performance_by_month"
    
    # Load urls from file
    urls = load_urls_from_file(PAGES_FILE_PATH)

    # Fetch page data and save to database
    load_page_data_by_month(START_DATE, END_DATE, urls)

    # Load records from database and generate .csv file
    generate_monthly_performance_csv(START_DATE, END_DATE, urls, MONTHLY_REPORTS_DIR)