from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import random
CHROME_PATH = "/usr/lib/chromium-browser/chromedriver"
assert os.path.exists(CHROME_PATH), "You need to download chromedriver and specify the location of chromedriver in util/scraper_util.py. Google how to download and find your chromedriver"
REFRESH_INTERVAL=50
class Scraper:
    def __init__(self):
        # Create a Chrome WebDriver instance
        chrome_service = ChromeService(CHROME_PATH)  # Replace with your chromedriver path
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        self.i = 0
    
    def download_page(self, url, save_location, check_fnc = None):
        self._refresh()
        
        success=False
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 6)
        try:
            # Open the webpage
            
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//html")))

            # Get the fully rendered HTML content
            page_source = self.driver.page_source

            # Save the HTML content to a local file
            with open(save_location, "w", encoding="utf-8") as file:
                file.write(page_source)

            if (check_fnc is not None) and (check_fnc(save_location)):
                raise Exception("Invalid content at URL")


            print(f"HTML content has been downloaded and saved to {save_location}.")
            success=True
        except Exception as e:
            print(e)
            print(f"Failed on {url}")
            print("Scraper Oops")


        
        return success
    def download_page_with_retry(self, url, save_location, retries = 3):
        for attempt in range(retries + 1):
            success = self.download_page(url,save_location)
            if success:
                return success
            if attempt == retries:
                return success
            print(f"Attempt {attempt+1} on {url}")
            print("Retrying ...")
            time.sleep(random.randint(1,4))
                

    def _refresh(self):
        self.i+=1
        if self.i >= REFRESH_INTERVAL:
            self.driver.quit()
            time.sleep(1)
            #raise Exception("Animator Oops")
            self.__init__()
    def close(self):
        self.driver.quit()


class Animator:
    def __init__(self):
        # Create a Chrome WebDriver instance
        chrome_service = ChromeService(CHROME_PATH)  # Replace with your chromedriver path
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
        self.base_dir = 'file://' + os.getcwd()
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        self.i = 0
    def snapshot(self,html_path,wdir):
        html_path = os.path.join(self.base_dir, html_path)
        wpath = os.path.join(wdir, str(self.i).zfill(5)+'.png')
        self.i +=1
        self._refresh()


        self.driver.get(html_path)
        wait = WebDriverWait(self.driver, 6)
        complete = False
        try:
            # Open the webpage
            
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//html")))
            complete = True
        except Exception as e:
            print(e)
            print("Reset")
            i = self.i
            self.driver.quit()
            
            time.sleep(1)
            self.__init__()
            self.i = i

        if complete:
            width = self.driver.execute_script("return document.body.scrollWidth")
            height = self.driver.execute_script("return document.body.scrollHeight")
            self.driver.set_window_size(width, height)
            screenshot = self.driver.get_screenshot_as_png()
            with open(wpath, 'wb') as file:
                file.write(screenshot)
            
        
            
    def _refresh(self):
        if (self.i % REFRESH_INTERVAL)==0:
            i = self.i
            self.driver.quit()
            print("Sleep")
            time.sleep(1)
            #raise Exception("Animator Oops")
            self.__init__()
            self.i = i


    def close(self):
        self.driver.quit()