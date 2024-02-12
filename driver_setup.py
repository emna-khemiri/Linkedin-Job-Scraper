from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class WebDriverSetup:
    def __init__(self):
        self.chrome_options = Options()
        # self.chrome_options.add_argument('--headless') # Uncomment if you run in headless mode
        self.driver = None

    def setup_driver(self):
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.maximize_window()
        return self.driver
