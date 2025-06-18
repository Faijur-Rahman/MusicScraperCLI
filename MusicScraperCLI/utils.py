import requests
from bs4 import BeautifulSoup
import time
from config import HEADERS

def get_page_soup(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            print(f"Fetching: {url}")
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt+1}/{max_retries}: Error fetching {url}: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
    return None
