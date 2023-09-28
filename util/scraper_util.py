from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class Scraper:

    @staticmethod
    def download_page(url, save_location):
        # Create a Chrome WebDriver instance
        chrome_service = ChromeService("/usr/lib/chromium-browser/chromedriver")  # Replace with your chromedriver path
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

            print(f"HTML content has been downloaded and saved to {save_location}.")
            success=True
        finally:
            # Close the WebDriver
            driver.quit()
        return success