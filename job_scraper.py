# job_scraper.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from settings import MAX_JOB_LISTINGS, SCROLL_PAUSE_TIME
from urllib.parse import urlparse
import time

class JobScraper:
    def __init__(self, driver):
        self.driver = driver
        self.job_details_df = pd.DataFrame(columns=["Job Title", "Company", "Location", "Post Date", "Work Type", "Job Link"])

    def scrape_jobs(self):
        job_links = self._collect_job_links()
        self._visit_each_job_and_collect_details(job_links)
        self.save_to_csv()

    def _collect_job_links(self):
        job_links = []
        job_listings = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.job-card-container__link.job-card-list__title')))
        for job_listing in job_listings[:MAX_JOB_LISTINGS]:
            job_links.append(job_listing.get_attribute('href'))
        return job_links

    def _visit_each_job_and_collect_details(self, job_links):
        idx, success_count = 0, 0
        while success_count < 20 and idx < len(job_links):
            try:
                print('job_link:  ', job_links[idx])
                self.driver.get(job_links[idx])
                time.sleep(10)  # Replace or adjust as necessary

                current_url = self.driver.current_url
                parsed_current_url = urlparse(current_url)
                parsed_job_link = urlparse(job_links[idx])

                if parsed_current_url.netloc == parsed_job_link.netloc and '/jobs/' in parsed_current_url.path and not parsed_current_url.path.endswith(parsed_job_link.path.split('/')[-1]):
                    print(f"Redirected to general jobs page for job link at index {idx}. Skipping to next.")
                    idx += 1
                    continue

                job_title = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1'))).text
                print('job_title:  ', job_title)
                details = self.driver.find_element(By.CSS_SELECTOR, '.job-details-jobs-unified-top-card__primary-description-without-tagline.mb2').text
                company_name = details.split('·')[0].strip()
                print('company_name:  ', company_name)
                company_location = details.split('·')[1].strip()
                print('company_location:  ', company_location)
                post_date = details.split('·')[2].strip()
                print('post_date:  ', post_date)
                work_type = self.driver.find_element(By.CSS_SELECTOR, 'li:nth-of-type(1) > span > span:nth-of-type(1)').text
                print('work_type:  ', work_type)

                self.job_details_df.loc[success_count] = {
                    "Job Title": job_title,
                    "Company": company_name,
                    "Location": company_location,
                    "Post Date": post_date,
                    "Work Type": work_type,
                    "Job Link": job_links[idx]
                }
                success_count += 1
            except Exception as e:
                print(f"Skipping job at index {idx} due to error: {e}")
            finally:
                idx += 1

    def save_to_csv(self):
        self.job_details_df.to_csv('data_analyst_jobs_saudi_arabia.csv', index=False)
        print(f"Scraping completed and data saved to 'data_analyst_jobs_saudi_arabia.csv'. Total jobs scraped: {len(self.job_details_df)}.")
