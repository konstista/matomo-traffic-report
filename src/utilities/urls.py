import re

def sanitize_url(url):
    # Remove query parameters
    url = re.sub(r'\?.*$', '', url)
    
    # Remove trailing whitespaces
    url = url.strip()
    
    # Remove trailing slash
    url = re.sub(r'/$', '', url)
    
    return url

def load_urls_from_file(file_path):
    sanitized_urls = []
    
    with open(file_path, 'r') as file:
        for line in file:
            url = line.strip()
            sanitized_url = sanitize_url(url)
            sanitized_urls.append(sanitized_url)
    
    return sanitized_urls