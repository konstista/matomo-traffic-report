from datetime import datetime, timedelta
from calendar import monthrange

def extract_date_ranges(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    date_ranges = []
    current = start
    
    while current <= end:
        month_start = current.replace(day=1)
        month_end = current.replace(day=monthrange(current.year, current.month)[1])
        range_end = min(month_end, end)
        
        is_full_month = (current == month_start and range_end == month_end)
        
        if month_end > end:
            month_end = end
        
        date_ranges.append({
            "start_date": current.strftime("%Y-%m-%d"),
            "end_date": month_end.strftime("%Y-%m-%d"),
            "is_full_month": is_full_month
        })
        
        if month_end == end:
            break
        
        current = (month_end + timedelta(days=1))
    
    return date_ranges

def extract_month(date):
    dt = datetime.strptime(date, "%Y-%m-%d")
    return dt.strftime("%Y-%m")