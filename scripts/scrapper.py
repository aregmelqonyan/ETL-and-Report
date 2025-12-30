import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config.logging_config import get_logger
from utils import utils

logger = get_logger(__name__)

class AutoAmScraper:
    def __init__(self, csv_file, start_page=1, end_page=3):
        self.csv_file = csv_file
        self.start_page = start_page
        self.end_page = end_page
        self.driver = None
        self.wait = None

        self._prepare_csv()
        self._init_driver()

    def _prepare_csv(self):
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, "w"):
                pass

    def _init_driver(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options,
        )

        self.wait = WebDriverWait(self.driver, 15)

    def _build_url(self, page):
        return (
            'https://auto.am/search/passenger-cars?q='
            '{"category":"1","page":"' + str(page) + '","sort":"latest","layout":"list",'
            '"user":{"dealer":"0","id":""},"year":{"gt":"1911","lt":"2026"},'
            '"usdprice":{"gt":"0","lt":"100000000"},'
            '"mileage":{"gt":"10","lt":"1000000"}}'
        )

    def scrape(self):
        for page in range(self.start_page, self.end_page):
            url = self._build_url(page)
            logger.info(f"Page {page}")

            self.driver.get(url)

            try:
                self.wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "list"))
                )
            except Exception:
                logger.info("No listings found, stopping.")
                break

            elements = self.driver.find_elements(By.CLASS_NAME, "list")

            for item in elements:
                utils.write_in_csv(item, "է", self.csv_file)

            time.sleep(2)

        self.close()
        logger.info("Scraping Done!")

    def close(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    csv_path = os.path.join(PROJECT_ROOT, "data", "raw", "data.csv")
    scraper = AutoAmScraper(
        csv_file=csv_path,
        start_page=1,
        end_page=3,
    )
    scraper.scrape()
