import logging
from datetime import datetime
import time
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
CHROME_DRIVER_PATH = "C:\\Users\\saeijou\\Downloads\\chromedriver.exe"
URL = "https://www.g2g.com/offer/Crusader-Strike--US---Seasonal----Alliance?service_id=lgc_service_1&brand_id=lgc_game_27816&region_id=dfced32f-2f0a-4df5-a218-1e068cfadffa&fa=lgc_27816_platform%3Algc_27816_platform_49642&sort=lowest_price&include_offline=1"
ELEMENT_ID = "precheckout_ppu_amount"
WAIT_TIME = 15
WINDOW_SIZE = (80, 60)
SLEEP_TIME = 30

def setup_driver() -> webdriver.Chrome:
    service = Service(CHROME_DRIVER_PATH)
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--log-level=3")
    return webdriver.Chrome(service=service, options=options)

def get_element_text(driver: webdriver.Chrome, element_id: str, wait_time: int) -> Optional[str]:
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
        return element.text.strip()
    except Exception as e:
        logger.error(f"Error getting element text: {e}")
        return None

def get_value_from_website(url: str) -> Optional[str]:
    with setup_driver() as driver:
        try:
            driver.get(url)
            driver.set_window_size(*WINDOW_SIZE)
            return get_element_text(driver, ELEMENT_ID, WAIT_TIME)
        except Exception as e:
            logger.error(f"Error in get_value_from_website: {e}")
            return None

def main():
    try:
        while True:
            result = get_value_from_website(URL)
            if result:
                logger.info(f"$/Gold Price on Crusader Strike: {result}")
            else:
                logger.warning("Failed to retrieve price")
            time.sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        logger.info("Script terminated by user")

if __name__ == "__main__":
    main()