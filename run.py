from dotenv import load_dotenv

from src.utilities.urls import load_urls_from_file
from src.scripts.load_page_data_by_month import load_page_data_by_month

if __name__ == '__main__':
    load_dotenv()
    
    START_DATE = "2023-10-01"
    END_DATE = "2024-10-23"
    FILE_PATH = "./data/pages.txt"
    
    # Load urls from file
    urls = load_urls_from_file(FILE_PATH)
    # Fetch page data and save to database
    load_page_data_by_month(START_DATE, END_DATE, urls)