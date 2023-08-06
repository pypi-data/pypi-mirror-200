import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import urllib.request
from selenium.common.exceptions import TimeoutException
import pandas as pd


class ScrapeLinkedInJob:
    def __init__(self, job_role, scroll_time):
        self.job_role = job_role.replace(' ', '+').lower()
        self.scroll_time = scroll_time
    def start_process(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.get(f"https://www.linkedin.com/jobs/search/?keywords={self.job_role}")
        time.sleep(5)
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_time = 1
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print("-----------scrolling---------")
            time.sleep(5)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height or scroll_time == self.scroll_time:
                print("same height")
                break
            last_height = new_height
            scroll_time += 1

        self.driver.execute_script("window.scrollTo(0, 0);")
        container = self.driver.find_element(By.CLASS_NAME,'jobs-search__results-list')
        self.links = container.find_elements(By.TAG_NAME, "a")
    def start_scraping(self):
        oe = 0
        self.actual_links = []
        self.job_name = []
        self.job_location = []
        self.job_uploaded = []
        self.job_description = []
        for link in self.links:
            if oe %2 == 0:
                temp = link.get_attribute('href')
                print(temp)
                self.actual_links.append(temp)
                link.click()
                print("clicked")
                time.sleep(2)
                print(link)
                print("Located")
                try:
                    self.job_name.append(link.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/a').text)
                    print(link.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/a').text)
                except:
                    self.job_name.append("None")
                try:
                    print(link.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[1]').text)
                    self.job_location.append(link.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[1]').text)
                except:
                    self.job_location.append("None")
                try:
                    print(link.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[2]/span[1]').text)
                    self.job_uploaded.append(link.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[2]/span[1]').text)
                except:
                    self.job_uploaded.append("None")
                try:
                    link.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/button[1]').click()
                except:
                    pass
                try:
                    print(link.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/div').text)
                    self.job_description.append(link.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/div').text)
                except:
                    self.job_description.append("None")
                oe+=1
            else:
                oe+=1
        
    def save_to_csv(self):
        df = pd.DataFrame({'Job Name': self.job_name, 'Job Location': self.job_location, 'Job Uploaded': self.job_uploaded, 'Job Description': self.job_description})
        df.to_csv(f'jobs_{self.job_role}.csv', index=False, encoding='utf-8')
        print("Saved to csv")
    
    def exit(self):
        self.driver.close()
        self.driver.quit()
    
    def scrape_job(self):
        self.start_process()
        self.start_scraping()
        self.save_to_csv()
        self.exit()



#### Testing

# if __name__ == "__main__":
#     job_role = "Machine Learning Engineer"
#     scroll_time = 1
#     obj = ScrapeLinkedInJob(job_role, scroll_time)
#     obj.scrape_job()