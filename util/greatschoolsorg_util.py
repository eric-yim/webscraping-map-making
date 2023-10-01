from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from util.scraper_util import Scraper
from util.usa_util import POP_CITIES
# BASE_URL = "https://www.greatschools.org/washington/schools/?gradeLevels%5B%5D=e"
BASE_FORMAT = "https://www.greatschools.org/{state}/schools/{gradelevel}{pagenumber}"
GRADE_LEVELS = {
    'elementary':'?gradeLevels%5B%5D=e',
    'middle':'?gradeLevels%5B%5D=m',
    'high':'?gradeLevels%5B%5D=h'
}

class GSO_Util:
    @staticmethod 
    def get_grade_level_str(grade):
        assert grade in GRADE_LEVELS, f"Grade {grade} not one of {GRADE_LEVELS.keys()}"
        return GRADE_LEVELS.get(grade)
    @staticmethod
    def get_page_number_str(page):
        assert int(page) > 0, f"Page {page} must be an integer greater than 0"
        page = int(page)
        if page == 1:
            return ""
        return f"&page={page}"
    @staticmethod
    def get_state_str(state):
        assert state.title() in POP_CITIES, f"Unkonwn state {state}"
        return state.lower()

    @staticmethod
    def get_url(state,grade,page):
        info = {
            'state': GSO_Util.get_state_str(state),
            'gradelevel': GSO_Util.get_grade_level_str(grade),
            'pagenumber': GSO_Util.get_page_number_str(page)
        }
        return BASE_FORMAT.format(**info)

    @staticmethod
    def get_school_links_in_html(fpath, state):
        base_url = "https://www.greatschools.org"
        link_startswith = f"/{state}"
        with open(fpath, 'r') as f:
            html_content = f.read()
        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        school_links = []
        # Find all <li> items with class "unsaved"
        unsaved_items = soup.find_all('li', class_='unsaved')

        for item in unsaved_items:
            # Find all <a> elements within the current item
            links = item.find_all('a')
            
            sub_links = []
            for link in links:
                href = link.get('href')
                if href.startswith(link_startswith):
                    sub_links.append(href)
            school_links.append(base_url + sub_links[0])
        return school_links