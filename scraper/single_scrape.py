# Selenium imports
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import sys

def glassdoor(query):
    options = webdriver.ChromeOptions()

    # uncomment below to activate headless
    options.add_argument('headless')
    options.add_argument('start-maximized')

    # install the driver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    # construct a url from keywords
    kw_param = '%20'.join(query.split(' '))
    url = f'https://www.glassdoor.com/Job/jobs.htm?sc.keyword={kw_param}'

    driver.get(url) # open jobs page

    job_listing = driver.find_element_by_class_name("react-job-listing") # gets first job listing

    job_info = job_listing.text.split('\n')

    # check to see if there is a rating, then remove it
    try:
        float(job_info[0])
        job_info.pop(0)
    except ValueError:
        pass
    
    job_company = job_info[0]
    job_title = job_info[1]
    job_location = job_info[2]

    # find job description
    job_description = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, './/div[@class="jobDescriptionContent desc"]'))).text

    # adds the listing to our jobs list
    return {
        "Company Name": job_company,
        "Job Title": job_title,
        "Job Location": job_location,
        "Job Description": job_description
    }


if __name__ == "__main__":
    print(glassdoor(str(sys.argv[1])))