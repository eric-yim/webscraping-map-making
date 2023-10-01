from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
CHROME_PATH = "/usr/lib/chromium-browser/chromedriver"
assert os.path.exists(CHROME_PATH), "You need to download chromedriver and specify the location of chromedriver in util/scraper_util.py. Google how to download and find your chromedriver"

class Scraper:

    @staticmethod
    def download_page(url, save_location, check_fnc = None):
        # Create a Chrome WebDriver instance
        chrome_service = ChromeService(CHROME_PATH)  # Replace with your chromedriver path
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

        # URL of the webpage you want to access
        # Replace with your URL
        
        success=False
        try:
            # Open the webpage
            driver.get(url)

            # Wait for the page to load completely (you can adjust the timeout as needed)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Get the fully rendered HTML content
            page_source = driver.page_source

            # Save the HTML content to a local file
            with open(save_location, "w", encoding="utf-8") as file:
                file.write(page_source)

            if (check_fnc is not None) and (check_fnc(save_location)):
                raise Exception("Invalid content at URL")


            print(f"HTML content has been downloaded and saved to {save_location}.")
            success=True
        except Exception:
            print("Scraper Oops")


        finally:
            # Close the WebDriver
            driver.quit()
        return success


