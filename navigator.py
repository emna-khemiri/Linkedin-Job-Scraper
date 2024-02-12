
from settings import JOB_SEARCH_URL
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from settings import SCROLL_PAUSE_TIME

class Navigator:
    def __init__(self, driver):
        self.driver = driver

    def navigate_to_job_search(self):
        self.driver.get(JOB_SEARCH_URL)
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.jobs-search-results-list')))

    def scroll_job_listings(self, job_listings_container):
        for _ in range(20):  
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 250;", job_listings_container)
            time.sleep(SCROLL_PAUSE_TIME)
