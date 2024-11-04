from dotenv import load_dotenv

from src.utilities.urls import load_urls_from_file

from src.scripts.load_page_data_by_month import load_page_data_by_month
from src.scripts.generate_monthly_performance_csv import generate_monthly_performance_csv
from src.scripts.load_website_traffic_per_month import load_website_traffic_per_month
from src.scripts.generate_website_monthly_dynamics_csv import generate_website_monthly_dynamics_csv
from src.scripts.load_top_pages_for_period import load_top_pages_for_period
from src.scripts.generate_top_pages_for_period_csv import generate_top_pages_for_period_csv

def generate_page_monthly(START_DATE, END_DATE):
    PAGES_FILE_PATH = "./data/pages.txt"
    
    # Reports
    REPORTS_DIR = "./reports/performance_by_month"
    
    # Load urls from file
    urls = load_urls_from_file(PAGES_FILE_PATH)

    # Fetch page data and save to database
    load_page_data_by_month(START_DATE, END_DATE, urls)

    # Load records from database and generate .csv file
    generate_monthly_performance_csv(START_DATE, END_DATE, urls, REPORTS_DIR)

def generate_website_monthly(START_DATE, END_DATE):
    REPORT_DIR = "./reports/website_traffic_by_month"
    
    # Fetch website data month by month and save to database
    load_website_traffic_per_month(START_DATE, END_DATE)
    
    # Load documents from database and create csv
    generate_website_monthly_dynamics_csv(START_DATE, END_DATE, REPORT_DIR)


def generate_pages_for_period(START_DATE, END_DATE):
    REPORT_DIR = "./reports/pages_for_range"
    
    # Fetch website data for period and save to database.
    # load_top_pages_for_period(START_DATE, END_DATE)

    # Load documents from database and create csv
    generate_top_pages_for_period_csv(START_DATE, END_DATE, REPORT_DIR)

if __name__ == '__main__':
    load_dotenv()
    
    START_DATE = "2023-10-01"
    END_DATE = "2024-10-31"
    
    # Generate report for a given page list that would contain monthly traffic
    # generate_page_monthly(START_DATE, END_DATE)
    
    # Generate report for a given date range that would contain total website traffic stats
    # generate_website_monthly(START_DATE, END_DATE)
    
    # Generate report for a given date range that shows most visited pages with its stats
    generate_pages_for_period(START_DATE, END_DATE)