from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from util.scraper_util import Scraper
BASE_URL = "https://www.greatschools.org/washington/schools/?gradeLevels%5B%5D=e"
BASE_SAVE = "school_paginations/"
def get_url(i):
    if i==1:
        return BASE_URL
    return BASE_URL + f'&page={i}'
def download_ith_page(i):
    url = get_url(i)
    save_location = os.path.join(BASE_SAVE, str(i).zfill(3) + ".html")
    return Scraper.download_page(url, save_location)
def main():
    os.makedirs(BASE_SAVE, exist_ok=True)
    # Iterate through 100 pages. if failed, break
    for i in range(1,101):
        if not (download_ith_page(i)):
            print(f"Failed at page {i}")
            break

if __name__=="__main__":
    main()


