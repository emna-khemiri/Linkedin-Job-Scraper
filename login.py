from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import LINKEDIN_LOGIN_URL, CREDENTIALS_PATH
import time

class LinkedInLogin:
    def __init__(self, driver):
        self.driver = driver

    def login(self):
        with open(CREDENTIALS_PATH, 'r', encoding="utf-8") as file:
            user_name, password = file.read().splitlines()

        self.driver.get(LINKEDIN_LOGIN_URL)
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.element_to_be_clickable((By.ID, 'username'))).send_keys(user_name)
        wait.until(EC.element_to_be_clickable((By.ID, 'password'))).send_keys(password)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-litms-control-urn='login-submit']"))).click()
        time.sleep(120)

