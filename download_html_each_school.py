from bs4 import BeautifulSoup
import glob, os
from util.scraper_util import Scraper
BASE_URL = "https://www.greatschools.org"
PAGINATION_HTMLS = "school_paginations/"
SCHOOL_HTMLS = "school_htmls/"
LINK_STARTSWITH = '/washington'
def get_school_links_in_html(fpath):
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
            if href.startswith(LINK_STARTSWITH):
                sub_links.append(href)
        school_links.append(sub_links[0])
    return school_links
def get_listing():
    return sorted(glob.glob(os.path.join(PAGINATION_HTMLS, "*.html")))
def main():
    os.makedirs(SCHOOL_HTMLS, exist_ok=True)
    listing = get_listing()
    j = 0
    for item in listing:
        school_links = get_school_links_in_html(item)
        for school_link in school_links:
            url = BASE_URL + school_link
            save_location = os.path.join(SCHOOL_HTMLS, str(j).zfill(5) + '.html')
            if not Scraper.download_page(url, save_location):
                print(f"Failed on {url}")
            j+=1
                



if __name__=='__main__':
    main()