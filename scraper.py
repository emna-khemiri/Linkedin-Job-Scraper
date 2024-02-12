
from driver_setup import WebDriverSetup
from login import LinkedInLogin
from navigator import Navigator
from job_scraper import JobScraper

def main():
    web_driver_setup = WebDriverSetup()
    driver = web_driver_setup.setup_driver()

    linkedin_login = LinkedInLogin(driver)
    linkedin_login.login()

    navigator = Navigator(driver)
    navigator.navigate_to_job_search()

    scraper = JobScraper(driver)
    scraper.scrape_jobs()
    scraper.save_to_csv()

    print("Scraping completed. Data saved to 'data_analyst_jobs_saudi_arabia.csv'.")
    driver.quit()

if __name__ == "__main__":
    main()
